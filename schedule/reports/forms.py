# -*- coding: utf-8 -*-
from datetime import datetime, date
from django import forms
from django.db.models import Q
from random import choice
from core.models import Department
from dateutil.relativedelta import relativedelta
import enums

TIMERANGE_CHOICES = (
    ('month', u'Текущий месяц'),
    ('year', u'Год'),
)

QUERY_CHOICES = (
    ('organization', u'По организациям'),
    ('department', u'По филиалам'),
    ('position', u'По должностям'),
    ('cast', u'По типам органзаций'),
    ('category', u'По категории слушателей'),
)


class ReportQueryForm(forms.Form):

    time_range = forms.ChoiceField(label=u'Временной интервал', choices=TIMERANGE_CHOICES, required=False)
    vertical = forms.ChoiceField(label=u'По вертикали', choices=QUERY_CHOICES)
    horizontal = forms.ChoiceField(label=u'По горизонтали', choices=QUERY_CHOICES)

    def get_timerange(self):
        choice = self.cleaned_data['time_range']
        today = date.today()

        if choice == 'month':
            return today.replace(day=25) + relativedelta(months=-1),  today.replace(day=25)
        if choice == 'year':
            return today.replace(month=1, day=1), today.replace(month=12, day=31)
