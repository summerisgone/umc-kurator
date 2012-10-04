# -*- coding: utf-8 -*-
from auth.models import Listener
from djangorestframework.views import View

class AutocompleteLastName(View):
    def get(self, request):
        return Listener.objects.filter(
            last_name__istartswith=request.GET.get('last_name','')
            ).values_list('last_name', flat=True)[:20]
