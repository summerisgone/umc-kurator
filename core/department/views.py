# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView, TemplateView
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

class StudyGroupMixin(DepartmentMixin):

    def get_studygroup(self):
        return get_object_or_404(StudyGroup, pk=self.kwargs['studygroup_pk'])

    def extra_context(self):
        context = super(StudyGroupMixin, self).extra_context()
        context.update({
            'studygroup': self.get_studygroup()
        })
        return context


class Index(ExtraContextMixin, DepartmentMixin, TemplateView):
    template_name='department/index.html'
    context_object_name='department'
    model = Department


class StudyGroupList(ExtraContextMixin, DepartmentMixin, ListView):
    model = StudyGroup
    template_name = 'department/studygroup_list.html'

    def get_queryset(self):
        return self.model.objects.all()  #filter(department=self.get_department())


class StudyGroupDetail(ExtraContextMixin, DepartmentMixin, DetailView):
    template_name = 'department/studygroup_detail.html'
    model = StudyGroup


class AddListener(ExtraContextMixin, StudyGroupMixin, FormView):
    template_name = 'department/listener_add.html'
    form_class = ListenerAddForm

    def get_form(self, form_class):
        return form_class(self.get_studygroup(), **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.get_studygroup().get_absolute_url()


class ListenerList(DepartmentMixin, ListView):
    template_name = 'department/listener_list.html'

    model = Listener

    def get_queryset(self):
        qs = super(ListenerList, self).get_queryset()
        return qs.filter(vizit__studygroup__department=self.get_department()).distinct()


class StudyGroupListenersList(StudyGroupMixin, ListView):

    model = Listener
    template_name = 'department/studygroup_listener_list.html'

    def get_queryset(self):
        queryset = super(StudyGroupListenersList, self).get_queryset()
        return queryset.filter(group=self.get_studygroup())


class ListenerBatchSelect(StudyGroupListenersList):

    template_name = 'department/listener_add_batch.html'

    def get_queryset(self):
        # все слушатели этого филиала
        return self.get_studygroup().department.listeners().filter(self.build_query())


class ListenerBatchApply(StudyGroupMixin, FormView):

    form_class = BatchListenersForm
    template_name = 'department/listener_add_batch.html'

    def form_valid(self, form):
        studygroup = self.get_studygroup()

        for listener in form.cleaned_data['listeners']:
            listener.apply_studygroup(studygroup)
            messages.add_message(self.request, messages.INFO, u'Добавлен слушатель %s' % listener)

        if 'next' in self.request.POST:
            return HttpResponseRedirect(self.request.POST['next'])
        else:
            return HttpResponseRedirect(studygroup.get_absolute_url())

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
