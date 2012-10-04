# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from os.path import join
from auth.models import Listener
from djangorestframework.views import View
from utils import firstcaps
from pymorphy import get_morph
from pymorphy.contrib import lastnames_ru


class AutoCompleteLastName(View):

    def get(self, request):
        return Listener.objects.filter(
            last_name__istartswith=firstcaps(self.PARAMS.get('term',''))
            ).values_list('last_name', flat=True).distinct()[:20]


class AutoCompleteFirstName(View):

    def get(self, request):
        return Listener.objects.filter(
            first_name__istartswith=firstcaps(self.PARAMS.get('term',''))
            ).values_list('first_name', flat=True).distinct()[:20]


class AutoCompletePatronymic(View):

    def get(self, request):
        return Listener.objects.filter(
            patronymic__istartswith=firstcaps(self.PARAMS.get('term',''))
            ).values_list('patronymic', flat=True).distinct()[:20]

class InflateForm(forms.Form):
    last_name = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    patronymic = forms.CharField(max_length=100)


class InflateNames(View):
    form = InflateForm

    def post(self, request):
        morph = get_morph(join(settings.PROJECT_DIR, 'morph'))
        last_name = self.DATA['last_name']
        first_name = self.DATA['first_name']
        patronymic = self.DATA['patronymic']

        # для склонения фамилии надо определить пол
        try:
            sex = morph.get_graminfo(first_name.upper())[0]['info'].split(',', 1)[0]
        except IndexError:
            # get_graminfo() вернул []
            sex = u'жр'
        # фамилия
        last_name_inflated = firstcaps(lastnames_ru.inflect(morph,
            last_name.upper(), u'дт'))
        # имя
        first_name_inflated = firstcaps(morph.inflect_ru(first_name.upper(), u'дт'))
        # отчество
        patronymic_inflated = firstcaps(morph.inflect_ru(patronymic.upper(), u'дт'))
        return {
            'last_name': last_name_inflated,
            'first_name': first_name_inflated,
            'patronymic': patronymic_inflated,
        }
