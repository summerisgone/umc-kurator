# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.forms.models import modelform_factory
from django.views.generic import ListView, DetailView, FormView, View, TemplateView, CreateView
from auth.models import Listener
from schedule.core.forms import AddListenerForm, CourseAddForm, EmitCertificateForm
from schedule.core.models import Department, Course, Certificate


class Index(TemplateView):
    template_name = 'core/index.html'

class CourseAdd(FormView):
    model = Course
    form_class = CourseAddForm
    template_name = 'core/course_form.html'

    def get_success_url(self):
        return self.get_department().get_absolute_url()

    def get_department(self):
        return get_object_or_404(Department, pk=self.kwargs['department_id'])

    def get_form(self, form_class):
        return form_class(self.get_department(), **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


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
            return self.render_to_response({'form': form})


class EmitCertificate(FormView):
    model = Certificate
    form_class = EmitCertificateForm
    template_name = 'core/certificate_form.html'

    def get_success_url(self):
        return self.get_course_and_listener()[0].get_absolute_url()

    def get_course_and_listener(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        listener = get_object_or_404(Listener, pk=self.kwargs['listener_id'])
        return course, listener

    def get_form(self, form_class):
        return form_class(*self.get_course_and_listener(), **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())
