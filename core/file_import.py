# -*- coding: utf-8 -*-
import random

from django.db.models import Q

from core import enums
from xlsimport.models import Format
from xlsimport.parsers import*
from auth.models import Listener
from core.models import Organization, Subject, Department, StudyGroup
from utils import get_position_fuzzy, get_organization_type, get_profile_fuzzy, get_category


class FIOCell(TextCellToStringParser):

    def to_python(self):
        fio = super(FIOCell, self).to_python()
        if len(fio.split(" ")) != 3:
            raise ValidationError(u"В колонке должны быть фамилия имя и отчество")
        else:
            return fio.split(" ")


class FewNumbersCell(TextCellToStringParser):

    def to_python(self):
        value = super(FewNumbersCell, self).to_python()
        value = value.strip()
        reg = re.compile('\s+')
        numbers = reg.split(value)
        if len(numbers) > 1:
            return ','.join(numbers)
        else:
            return numbers


class ListenerFileFormat(Format):
    u"""Формат файла слушателей"""
    start_line = 1
    cells = (
        {'name': u'Предмет', 'parsers': (TextCellToStringParser,)},
        {'name': u'Кол-во часов', 'parsers': (TextCellToIntParser, NumberCellToIntParser)},
        {'name': u'Дата начала курса', 'parsers': (DateCellToDateParser, TextCellToDateParser)},
        {'name': u'Дата завершения курса', 'parsers': (DateCellToDateParser, TextCellToDateParser)},
        {'name': u'Район', 'parsers': (TextCellToStringParser,)},
        {'name': u'ФИО', 'parsers': (FIOCell,)},
        {'name': u'Организация', 'parsers': (TextCellToStringParser,)},
        {'name': u'Должность', 'parsers': (TextCellToStringParser,)},
        {'name': u'Курсовая работа', 'parsers': (TextCellToStringParser,)},
        {'name': u'Документ', 'parsers': (TextCellToIntParser, NumberCellToIntParser)},
    )

    def to_python(self, data_row):
        studygorup = dict(
            hours=data_row[1],
            start=data_row[2],
            end=data_row[3],
        )
        studygroup_query =  studygorup.copy()
        studygroup_query.update(dict(
            subject__short_name=data_row[0],
            department__name=data_row[4],
        ))

        subject = dict(
            short_name=data_row[0],
        )

        department = dict(
            name=data_row[4],
        )

        organization_name = data_row[6]
        match = re.findall(r'\d+', organization_name)
        organization_cast = get_organization_type(organization_name)
        organization = dict(
            name=organization_name,
            number=match[0] if match else None,
            cast=organization_cast,
        )

        last_name, first_name, patronymic = data_row[5]

        listener_position=get_position_fuzzy(data_row[7])
        listener = dict(
            first_name_inflated=first_name,
            last_name_inflated=last_name,
            patronymic_inflated=patronymic,
            position=listener_position,
            profile=get_profile_fuzzy(data_row[7]),
            category=get_category(organization_cast, listener_position),
        )

        attestation_work_name = data_row[8]
        cert_number = data_row[9]
        return {
            'studygroup': studygorup,
            'studygroup_query': studygroup_query,
            'department': department,
            'subject': subject,
            'listener': listener,
            'organization': organization,
            'attestation_work_name': attestation_work_name,
            'cert_number': cert_number,
        }


class SubjectFormat(Format):
    u"""Формат файла предметов"""
    cells = (
        {'name': u'Название', 'parsers': (TextCellToStringParser,)},
        {'name': u'Кол-во часов', 'parsers': (FewNumbersCell,
                                              TextCellToIntParser,
                                              NumberCellToIntParser,
                                              )},
        {'name': u'Краткое название', 'parsers': (TextCellToStringParser,)},
    )

    def to_python(self, data_row):
        return {
            'name': data_row[0],
            'short_name': re.sub(r'[0-9-]+', '', data_row[2]),
            'hours': data_row[1],
        }


class ListenerImportLogic(object):
    u"""Бизнес-логика испортирования слушателей"""
    errors = []

    def __init__(self, format_doc):
        self.doc = format_doc

    def process_row(self, index, parsed_row):
        if any([issubclass(type(cell), Exception) for cell in parsed_row]):
            self.errors.append((parsed_row, index + self.doc.start_line))
        else:
            self.save_row(self.doc.to_python(parsed_row))

    def save_row(self, row_data):
        # Найти или создать группу
        try:
            studygroup = StudyGroup.objects.get(**row_data['studygroup_query'])
        except StudyGroup.DoesNotExist:
            studygroup = self.create_study_group(row_data)

        # Найти или создать слушателя
        try:
            listener = Listener.objects.get(**row_data['listener'])
        except Listener.DoesNotExist:
            listener = self.create_listener(row_data)

        # Зарегистрировать слушателя в группе и выдать ему сертификат
        if listener.apply_studygroup(studygroup):
            # если уже в этой группе, ничего не обновлять
            listener.attest(studygroup, row_data['attestation_work_name'])
            listener.complete_course(studygroup)
            listener.issue_certificate(studygroup, row_data['cert_number'])

    def create_study_group(self, row_data):
        studygroup = StudyGroup(**row_data['studygroup'])
        studygroup.department = Department.objects.get(**row_data['department'])
        studygroup.subject = Subject.objects.get(**row_data['subject'])
        studygroup.status = enums.StudyGroupStatus.Closed
        studygroup.save()
        return studygroup


    def create_listener(self, row_data):
        organization, organization_created = Organization.objects.get_or_create(**row_data['organization'])
        if organization_created:
            organization.save()

        listener = Listener(**row_data['listener'])
        listener.organization = organization
        listener.username = 'user-%6d' % random.randint(0, 999999)
        listener.save()
        return listener


class SubjectImportLogic(object):
    u"""Бизнес-логика испортирования предметов"""
    errors = []

    def __init__(self, format_doc):
        self.doc = format_doc

    def process_row(self, index, parsed_row):
        if any([issubclass(type(cell), Exception) for cell in parsed_row]):
            self.errors.append((parsed_row, index + self.doc.start_line))
        else:
            subject = self.doc.to_python(parsed_row)
            self.save_row(subject)

    def save_row(self, subject_dict):
        # check is listener already in db
        query = Q(
            name__iexact=subject_dict['name'],
            short_name__iexact=subject_dict['short_name'],
            hours=subject_dict['hours'],
        )

        if not Subject.objects.filter(query).exists():
            return Subject.objects.create(**subject_dict)
