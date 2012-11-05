# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from core.models import Department

class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        return {
            'departments': Department.objects.all(),
        }