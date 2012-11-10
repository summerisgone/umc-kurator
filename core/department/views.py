# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from core.auth.models import Listener
from forms import ListenerAddForm, BatchListenersForm
from core.models import Department, StudyGroup, Organization
from utils import ExtraContextMixin


class DepartmentMixin(object):

    def get_department(self):
        return get_object_or_404(Department, pk=self.kwargs['department_id'])

    def extra_context(self):
        return {
            'department': self.get_department()
        }

class CourseMixin(DepartmentMixin):

    def get_course(self):
        return get_object_or_404(StudyGroup, pk=self.kwargs['course_pk'])

    def extra_context(self):
        context = super(CourseMixin, self).extra_context()
        context.update({
            'course': self.get_course()
        })
        return context



class CourseList(ExtraContextMixin, DepartmentMixin, ListView):
    model = StudyGroup
    template_name = 'department/course_list.html'

    def get_queryset(self):
        return self.model.objects.all()  #filter(department=self.get_department())


class CourseDetail(ExtraContextMixin, DepartmentMixin, DetailView):
    template_name = 'department/course_detail.html'
    model = StudyGroup


class AddListener(ExtraContextMixin, CourseMixin, FormView):
    template_name = 'department/listener_add.html'
    form_class = ListenerAddForm

    def get_form(self, form_class):
        return form_class(self.get_course(), **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.get_course().get_absolute_url()


class ListenerList(DepartmentMixin, ListView):
    template_name = 'department/listener_list.html'

    model = Listener

    def get_queryset(self):
        qs = super(ListenerList, self).get_queryset()
        return qs.filter(vizit__course__department=self.get_department()).distinct()


class CourseListenersList(CourseMixin, ListView):

    model = Listener
    template_name = 'department/course_listener_list.html'

    def get_queryset(self):
        queryset = super(CourseListenersList, self).get_queryset()
        return queryset.filter(course=self.get_course())


class ListenerBatchSelect(CourseListenersList):

    template_name = 'department/listener_add_batch.html'

    def get_queryset(self):
        # все слушатели этого филиала
        return self.get_course().department.listeners().filter(self.build_query())


class ListenerBatchApply(CourseMixin, FormView):

    form_class = BatchListenersForm
    template_name = 'department/listener_add_batch.html'

    def form_valid(self, form):
        course = self.get_course()

        for listener in form.cleaned_data['listeners']:
            listener.apply_course(course)
            messages.add_message(self.request, messages.INFO, u'Добавлен слушатель %s' % listener)

        if 'next' in self.request.POST:
            return HttpResponseRedirect(self.request.POST['next'])
        else:
            return HttpResponseRedirect(course.get_absolute_url())

    def form_invalid(self, form):
        context = self.get_context_data()
        context.update({
            'form': form,
        })

        return self.render_to_response(context)


class OrganizationList(ExtraContextMixin, DepartmentMixin, ListView):
    model = Organization
    template_name = 'department/organization_list.html'

    def get_queryset(self):
        return self.get_department().organizations()


class OrganizationDetail(ExtraContextMixin, DepartmentMixin, DetailView):
    model = Organization
    template_name = 'department/organization_detail.html'