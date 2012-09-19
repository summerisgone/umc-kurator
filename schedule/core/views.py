# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from schedule.core.models import Department

class DepartmentList(ListView):
    template_name = 'core/index.html'
    model = Department


class DepartmentDetail(DetailView):
    model = Department