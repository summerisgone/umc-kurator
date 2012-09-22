# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView, View, TemplateView
from schedule.core.forms import AddListenerForm
from schedule.core.models import Department, Course


class DepartmentList(ListView):
    template_name = 'core/index.html'
    model = Department


class DepartmentDetail(DetailView):
    model = Department


class CourseDetail(DetailView):
    model = Course


class AddListener(TemplateView):
    template_name = 'core/add_listener.html'

    def dispatch(self, request, course_pk, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=course_pk)
        return super(AddListener, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        return {'form': AddListenerForm(self.course)}

    def post(self, *args, **kwds):
        form = AddListenerForm(self.course, self.request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.course.get_absolute_url())
        else:
            return {'form': form}
