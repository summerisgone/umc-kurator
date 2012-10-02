# coding=utf-8
from django.views.generic import TemplateView


class ReportList(TemplateView):
    template_name = 'reports/index.html'