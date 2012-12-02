# -*- coding: utf-8 -*-
from datetime import date
from django import forms
from dateutil.relativedelta import relativedelta
from core.models import Department, Subject
from reports.query import PARAMETERS


QUERY_CHOICES = [(key, unicode(param())) for key, param in PARAMETERS.iteritems()]


class ReportQueryForm(forms.Form):

    vertical = forms.ChoiceField(label=u'По вертикали', choices=QUERY_CHOICES)
    horizontal = forms.ChoiceField(label=u'По горизонтали', choices=QUERY_CHOICES)
    grouping = forms.ChoiceField(label=u'Группировка', choices=QUERY_CHOICES)


class DepartmentForm(forms.Form):

    department = forms.ModelChoiceField(queryset=Department.objects.all(), label=u'Структурное подразделение')


class SubjectForm(forms.Form):

    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label=u'Программа')
