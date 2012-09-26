# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from schedule.auth.models import Profile
from schedule.core.models import Organization, Vizit, Course
import random


class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('subject', 'start', 'end', 'hours')

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.min.js',)

    def __init__(self, department, *args, **kwds):
        super(CourseAddForm, self).__init__(*args, **kwds)
        self.department = department
        self.fields['start'].widget = forms.TextInput(attrs={'data-datepicker': 'datepicker'})
        self.fields['end'].widget = forms.TextInput(attrs={'data-datepicker': 'datepicker'})

    def save(self, **kwds):
        self.instance.department = self.department
        super(CourseAddForm, self).save(**kwds)


class AddListenerForm(forms.Form):
    # User creation fields
    last_name = forms.CharField(label=u'Фамилия')
    first_name = forms.CharField(label=u'Имя')
    patronymic = forms.CharField(label=u'Отчество')

    organization = forms.CharField(label=u'Организация')

    def __init__(self, course, *args, **kwds):
        self.course = course
        super(AddListenerForm, self).__init__(*args, **kwds)

    def save(self):
        user = User.objects.create(
            username='user-%6d' % random.randint(0, 999999),
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        organization, created = Organization.objects.get_or_create(
            name=self.cleaned_data['organization']
        )
        profile = Profile.objects.create(
            user=user,
            organization=organization
        )
        Vizit.objects.create(course=self.course, user=user)