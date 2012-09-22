# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import random
from schedule.auth.models import Profile
from schedule.core.models import Organization, Vizit


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