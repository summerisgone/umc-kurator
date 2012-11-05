# -*- coding: utf-8 -*-
from core.models import Organization, Department
from core import enums


class AbstractParameter(object):

    def process_queryset(self, queryset, value):
        return queryset

    def values(self):
        pass


class DepartmentParameter(AbstractParameter):

    def process_queryset(self, queryset, department):
        return queryset.filter(course__department=department)

    def values(self):
        for dep in Department.objects.all():
            yield (dep.name, dep)

    def __unicode__(self):
        return u'Филиал'


class OrganizationParameter(AbstractParameter):

    def process_queryset(self, queryset, organization):
        return queryset.filter(organization=organization)

    def values(self):
        for org in Organization.objects.all():
            yield (org.name, org)

    def __unicode__(self):
        return u'Организация'


class PositionParameter(AbstractParameter):

    def process_queryset(self, queryset, position):
        return queryset.filter(position=position)

    def values(self):
        return enums.LISTENER_POSITIONS

    def __unicode__(self):
        return u'Должность'


class OrganizationCastParameter(AbstractParameter):

    def process_queryset(self, queryset, cast):
        return queryset.filter(organization__cast=cast)

    def values(self):
        return enums.ORGANIZATION_TYPES

    def __unicode__(self):
        return u'Тип организации'


class CategoryParameter(AbstractParameter):

    def process_queryset(self, queryset, category):
        return queryset.filter(category=category)

    def values(self):
        return enums.LISTENER_CATEGORIES

    def __unicode__(self):
        return u'Категория слушателя'

PARAMETERS = {
    'department': DepartmentParameter,
    'organization': OrganizationParameter,
    'position': PositionParameter,
    'cast': OrganizationCastParameter,
    'category': CategoryParameter,
}


class ResultTable(object):

    def __init__(self, row_param, col_param, queryset):
        self.row_param = row_param
        self.col_param = col_param
        self.queryset = queryset

        row_values = [val for val in row_param.values()]
        self.row_header = [val[0] for val in row_values]
        self.row_values = [val[1] for val in row_values]

        col_values = [val for val in col_param.values()]
        self.col_header = [val[0] for val in col_values]
        self.col_values = [val[1] for val in col_values]

        self.data = []

    def process(self):
        for i, row_value in enumerate(self.row_values):
            self.data.append([])
            for j, col_value in enumerate(self.col_values):
                qs = self.col_param.process_queryset(self.queryset, col_value)
                qs = self.row_param.process_queryset(qs, row_value)
                self.data[i].append(qs.count())
        return self.data

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

        data['table'] = self.data
        return data
