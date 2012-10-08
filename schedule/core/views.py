# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.forms.models import modelform_factory
from django.views.generic import ListView, DetailView, FormView, View, TemplateView, CreateView
from django.views.generic.edit import BaseFormView
from auth.models import Listener
from auth.views import ListenersList
from schedule.core.forms import ListenerAddForm, CourseAddForm, EmitCertificateForm, BatchListenersForm
from schedule.core.models import Department, Course, Certificate


class Index(TemplateView):
    template_name = 'core/index.html'

class CourseAdd(FormView):
    form_class = CourseAddForm
    template_name = 'core/course_add.html'

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


class CourseListenersList(ListenersList):

    def get_course(self):
        return get_object_or_404(Course, pk=self.kwargs['course_pk'])

    def get_queryset(self):
        queryset = super(CourseListenersList, self).get_queryset()
        return queryset.filter(course=self.get_course())

    def extra_context(self):
        return {'course': self.get_course()}


class ListenerBatchSelect(CourseListenersList):

    template_name = 'core/add_listener_batch.html'

    def extra_context(self):
        params = self.request.GET.copy()
        if 'page' in params:
            del(params['page'])
        get_params = params.urlencode()
        return {'get_params': get_params, 'course': self.get_course()}

    def get_queryset(self):
        # все слушатели этого филиала
        return self.get_course().department.listeners().filter(self.build_query())


class ListenerBatchUpdate(FormView):

    form_class = BatchListenersForm
    template_name = 'core/add_listener_batch.html'

    def get_course(self):
        return get_object_or_404(Course, pk=self.kwargs['course_pk'])

    def extra_context(self):
        return {'course': self.get_course()}

    def get_context_data(self, **kwargs):
        context = super(ListenerBatchUpdate, self).get_context_data(**kwargs)
        context.update(self.extra_context())
        return context

    def form_valid(self, form):
        course = self.get_course()

        for listener in form.cleaned_data['listeners']:
            listener.apply_course(course)
            # TODO: leave a message

        if 'next' in self.request.POST:
            return HttpResponseRedirect(self.request.POST['next'])
        else:
            return course.get_absolute_url()
