# -*- coding: utf-8 -*-
from auth.models import Listener
from djangorestframework.views import View
from utils import firstcaps

class AutoCompleteLastName(View):

    def get(self, request):
        return Listener.objects.filter(
            last_name__istartswith=firstcaps(request.GET.get('term',''))
            ).values_list('last_name', flat=True).distinct()[:20]


class AutoCompleteFirstName(View):

    def get(self, request):
        return Listener.objects.filter(
            first_name__istartswith=firstcaps(request.GET.get('term',''))
            ).values_list('first_name', flat=True).distinct()[:20]


class AutoCompletePatronymic(View):

    def get(self, request):
        return Listener.objects.filter(
            patronymic__istartswith=firstcaps(request.GET.get('term',''))
            ).values_list('patronymic', flat=True).distinct()[:20]
