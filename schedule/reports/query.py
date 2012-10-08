# -*- coding: utf-8 -*-
from core.models import Organization, Department
import enums


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


class OrganizationParameter(AbstractParameter):

    def process_queryset(self, queryset, organization):
        return queryset.filter(organization=organization)

    def values(self):
        for org in Organization.objects.all():
            yield (org.name, org)


class PositionParameter(AbstractParameter):

    def process_queryset(self, queryset, position):
        return queryset.filter(position=position)

    def values(self):
        return enums.LISTENER_POSITIONS


class OrganizationCastParameter(AbstractParameter):

    def process_queryset(self, queryset, cast):
        return queryset.filter(organization__cast=cast)

    def values(self):
        return enums.ORGANIZATION_TYPES


class CategoryParameter(AbstractParameter):

    def process_queryset(self, queryset, category):
        return queryset.filter(category=category)

    def values(self):
        return enums.LISTENER_CATEGORIES

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
