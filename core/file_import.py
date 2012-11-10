# -*- coding: utf-8 -*-
from django.db.models import Q
from xlsimport.models import Format
from xlsimport.parsers import*
from auth.models import Listener, Employee
from core.models import Organization, Certificate, Vizit, Subject
from utils import get_position_fuzzy, get_organization_type
import random


class FIOCell(TextCellToStringParser):

    def to_python(self):
        fio = super(FIOCell, self).to_python()
        if len(fio.split(" ")) != 3:
            raise ValidationError(u"В колонке должны быть фамилия имя и отчество")
        else:
            return fio.split(" ")


class ListenerFileFormat(Format):
    u"""Формат файла слушателей"""

    cells = (
        {'name': u'ФИО', 'parsers': (FIOCell,)},
        {'name': u'Организация', 'parsers': (TextCellToStringParser,)},
        {'name': u'Район', 'parsers': dummy_parsers},
        {'name': u'Должность', 'parsers': (TextCellToStringParser,)},
        {'name': u'Курсовая работа', 'parsers': dummy_parsers},
        {'name': u'Документ', 'parsers': (TextCellToStringParser,)},
    )

    def to_python(self, data_row):
        last_name, first_name, patronymic = data_row[0]
        listener = Listener(
            first_name_inflated=first_name,
            last_name_inflated=last_name,
            patronymic_inflated=patronymic,
            position=get_position_fuzzy(data_row[3]),
        )
        match = re.findall(r'\d+', data_row[1])

        organization = dict(
            name=data_row[1],
            number=match[0] if match else None,
            cast=get_organization_type(data_row[1]),
        )

        document = dict(
            name=data_row[5]
        )
        return listener, organization, document


class SubjectFormat(Format):
    u"""Формат файла предметов"""
    cells = (
        {'name': u'Название', 'parsers': (TextCellToStringParser,)},
        {'name': u'Кол-во часов', 'parsers': (TextCellToIntParser, NumberCellToIntParser,)},
        {'name': u'Краткое название', 'parsers': (TextCellToStringParser,)},
    )

    def to_python(self, data_row):
        return {
            'name': data_row[0],
            'short_name': data_row[2],
            'hours': data_row[1],
            'teacher': Employee.objects.all()[0] if Employee.objects.exists() else None,
        }


class ListenerImportLogic(object):
    u"""Бизнес-логика испортирования слушателей"""
    errors = []

    def __init__(self, format_doc, course):
        self.doc = format_doc
        self.course = course

    def process_row(self, index, parsed_row):
        if any([issubclass(type(cell), Exception) for cell in parsed_row]):
            self.errors.append((parsed_row, index + self.doc.start_line))
        else:
            listener, organization, document_data = self.doc.to_python(parsed_row)
            self.save_row(listener, organization, document_data)

    def register_listener(self, document_data, listener):
        # добавить слушателя к курсу
        Vizit.objects.create(
            course=self.course,
            listener=listener
        )

        # создать сертификат
        Certificate.objects.create(
            name=document_data['name'],
            course=self.course,
            listener=listener
        )

    def save_row(self, listener, organization_data, document_data):
        # check is listener already in db
        query = Q(
            last_name_inflated__iexact=listener.last_name_inflated,
            first_name_inflated__iexact=listener.first_name_inflated,
            patronymic_inflated__iexact=listener.patronymic_inflated,
        )

        if Listener.objects.filter(query).exists():
            listener = Listener.objects.filter(query)[0]
            self.register_listener(document_data, listener)
            return listener
        else:
            # get or create organization
            organization, created = Organization.objects.get_or_create(**organization_data)
            listener.organization = organization
            listener.username = 'user-%6d' % random.randint(0, 999999),

            # зарегистрировать
            listener.save()
            self.register_listener(document_data, listener)

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