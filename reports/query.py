# -*- coding: utf-8 -*-
from core.models import Organization, Department, Subject
from core import enums
from datetime import date


class AbstractParameter(object):

    def process_queryset(self, queryset, value):
        return queryset

    def values(self):
        pass


class DepartmentParameter(AbstractParameter):

    def process_queryset(self, queryset, department):
        return queryset.filter(group__department=department)

    def values(self):
        for dep in Department.objects.all():
            yield (dep.name, dep)

    def __unicode__(self):
        return u'Филиал'


class OrganizationParameter(AbstractParameter):

    def process_queryset(self, queryset, organization):
        return queryset.filter(listener__organization=organization)

    def values(self):
        for org in Organization.objects.all():
            yield (org.name, org)

    def __unicode__(self):
        return u'Организация'


class PositionParameter(AbstractParameter):

    def process_queryset(self, queryset, position):
        return queryset.filter(listener__position=position)

    def values(self):
        return enums.LISTENER_POSITIONS

    def __unicode__(self):
        return u'Должность'


class OrganizationCastParameter(AbstractParameter):

    def process_queryset(self, queryset, cast):
        return queryset.filter(listener__organization__cast=cast)

    def values(self):
        return enums.ORGANIZATION_TYPES

    def __unicode__(self):
        return u'Тип организации'


class CategoryParameter(AbstractParameter):

    def process_queryset(self, queryset, category):
        return queryset.filter(listener__category=category)

    def values(self):
        return enums.LISTENER_CATEGORIES

    def __unicode__(self):
        return u'Категория слушателя'


class TimeRangeParameter(AbstractParameter):

    def process_queryset(self, queryset, value):
        date_start, date_end = value
        return queryset.filter(group__start__gte=date_start, group__end__lte=date_end)

    def values(self):
        current_year = date.today().year
        values = []
        # 1 квартал
#        values.append((u'1 квартал', (date(current_year, 1, 1), date(current_year, 4, 1))))
        # 2 квартал
#        values.append((u'2 квартал', (date(current_year, 4, 1), date(current_year, 7, 1))))
        # 3 квартал
#        values.append((u'3 квартал', (date(current_year, 7, 1), date(current_year, 10, 1))))
        # 4 квартал
#        values.append((u'4 квартал', (date(current_year, 10, 1), date(current_year+1, 1, 1))))

        # 1 полугодие
        values.append((u'1 полугодие', (date(current_year, 1, 1), date(current_year, 7, 1))))
        # 2 полугодие
        values.append((u'2 полугодие', (date(current_year, 7, 1), date(current_year+1, 1, 1))))
        for value in values:
            yield value

    def __unicode__(self):
        return u'Кварталы'


class SubjectParameter(AbstractParameter):

    def process_queryset(self, queryset, subject):
        return queryset.filter(group__subject=subject)

    def values(self):
        for subject in Subject.objects.all():
            yield (subject.short_name, subject.id)

    def __unicode__(self):
        return u'Учебная программа'


PARAMETERS = {
    'department': DepartmentParameter,
    'organization': OrganizationParameter,
    'position': PositionParameter,
    'cast': OrganizationCastParameter,
    'category': CategoryParameter,
    'time_range': TimeRangeParameter,
    'subject': SubjectParameter,
}


class ResultTable(object):

    def __init__(self, row_param, col_param, grouping, queryset):
        self.row_param = row_param
        self.col_param = col_param
        self.grouping_param = grouping
        self.queryset = queryset

        row_values = [val for val in row_param.values()]
        self.row_header = [val[0] for val in row_values]
        self.row_values = [val[1] for val in row_values]

        col_values = [val for val in col_param.values()]
        self.col_header = [val[0] for val in col_values]
        self.col_values = [val[1] for val in col_values]

        self.data = []

    def process(self):
        for group_header, group_value in self.grouping_param.values():
            queryset = self.grouping_param.process_queryset(self.queryset, group_value)
            group_data = self.process_group(queryset)
            self.data.append({
                'group_header': group_header,
                'data': group_data,
            })

    def process_group(self, queryset):
        group_data = []
        for i, row_value in enumerate(self.row_values):
            group_data.append([])
            for j, col_value in enumerate(self.col_values):
                qs = self.row_param.process_queryset(queryset, row_value)
                qs = self.col_param.process_queryset(qs, col_value)
                group_data[i].append(qs.count())
        return group_data

    def to_dict(self):
        if not self.data:
            return {}
        data = {}
        data['meta'] = {
            'vertical': unicode(self.row_param),
            'horizontal': unicode(self.col_param),
            'row_header': self.row_header,
            'col_header': self.col_header,
        }

        data['tables'] = self.data
        return data
