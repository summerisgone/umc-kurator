# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.db.models import Q
from core.models import Department
from dateutil.relativedelta import relativedelta
import enums

TIMERANGE_CHOICES = (
    ('month', u'Текущий месяц'),
#    ('quarter', u'Квартал'),
#    ('halfyear', u'Полугодие'),
#    ('year', u'Год'),
)

class ReportQueryForm(forms.Form):

    time_range = forms.ChoiceField(label=u'Временной интервал', choices=TIMERANGE_CHOICES, required=False)
    department = forms.ModelChoiceField(label=u'Филиал', queryset=Department.objects.all(), required=False)
    listener_category = forms.ChoiceField(label=u'Категория слушателей', choices=enums.LISTENER_CATEGORIES, required=False)
    organization_type = forms.ChoiceField(label=u'Тип организации', choices=enums.ORGANIZATION_TYPES, required=False)

    def get_timerange(self, time_range):
        now = datetime.now()
        if time_range == 'month':
            end = now.replace(day=25)
            start = end - relativedelta(months=-1)
        return start, end

    def get_query(self):
        # query - запрос к курсу
        query = Q()
        if 'time_range' in self.cleaned_data and self.cleaned_data['time_range']:
            start, end = self.get_timerange(self.cleaned_data['time_range'])
            query &= Q(start__gt=start) and Q(end__lte=end)
#        if 'department' in self.cleaned_data and self.cleaned_data['department']:
#            query &= Q(department=self.cleaned_data['department'])
#        if 'listener_category' in self.cleaned_data and self.cleaned_data['listener_category']:
#            query &= Q(students__category__exact=self.cleaned_data['listener_category'])
#        if 'organization_type' in self.cleaned_data and self.cleaned_data['organization_type']:
#            query &= Q(students__organization__cast__exact=
#                self.cleaned_data['organization_type'])
        return query