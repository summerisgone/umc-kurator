# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.forms.models import modelform_factory
from django.views.generic import ListView, DetailView, FormView, View, TemplateView, CreateView
from django.views.generic.edit import BaseFormView
from auth.models import Listener
from schedule.core.forms import ListenerAddForm, CourseAddForm, EmitCertificateForm
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


class AddListener(FormView):
    template_name = 'core/add_listener.html'
    form_class = ListenerAddForm

    def get_course(self):
        return get_object_or_404(Course, pk=self.kwargs['course_pk'])

    def get_form(self, form_class):
        return form_class(self.get_course(), **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.get_course().get_absolute_url()


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


class ListenersList(ListView):
    model = Listener
    paginate_by = 50

    def get_course(self):
        return get_object_or_404(Course, pk=self.kwargs['course_pk'])

    def get_queryset(self):
        return self.model.objects.filter(course=self.get_course())

    def get_context_data(self, **kwargs):
        context = super(ListenersList, self).get_context_data(**kwargs)
        context.update({
            'course': self.get_course()
        })
        return context