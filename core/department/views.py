# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django.forms.models import modelformset_factory
from core import enums
from core.auth.models import Listener
from crud.views import ListExtras
from forms import ListenerAddForm, BatchListenersForm
from core.models import Department, StudyGroup, Organization, Vizit
from utils import ExtraContextMixin


class DepartmentFromUrl(object):

    def get_department(self):
        return get_object_or_404(Department, pk=self.kwargs['department_id'])

    def extra_context(self):
        return {
            'department': self.get_department()
        }

class DepartmentMixin(ExtraContextMixin, DepartmentFromUrl):
    pass

class StudyGroupMixin(DepartmentMixin):

    def get_studygroup(self):
        return get_object_or_404(StudyGroup, pk=self.kwargs['studygroup_pk'])

    def extra_context(self):
        context = super(StudyGroupMixin, self).extra_context()
        context.update({
            'studygroup': self.get_studygroup()
        })
        return context


class Index(DepartmentMixin, TemplateView):
    template_name='department/index.html'
    context_object_name='department'
    model = Department


class StudyGroupList(DepartmentMixin, ListView):
    model = StudyGroup
    template_name = 'department/studygroup_list.html'

    def get_queryset(self):
        return self.model.objects.order_by('status', 'start', 'id')


class StudyGroupDetail(DepartmentMixin, DetailView):
    template_name = 'department/studygroup_detail.html'
    model = StudyGroup


class StudyGroupComplete(DepartmentMixin, SingleObjectMixin, View):
    model = StudyGroup

    def post(self, request, *args, **kwargs):
        group = self.get_object()
        group.status = enums.StudyGroupStatus.Complected
        group.save()
        messages.add_message(self.request, messages.INFO, u'Набор в группу %s завершен' % group)
        return HttpResponseRedirect(reverse("department:studygroup_detail", kwargs=kwargs))


class ListenerList(DepartmentMixin, ListExtras, ListView):
    template_name = 'department/listener_list.html'
    model = Listener

    def get_queryset(self):
        qs = super(ListenerList, self).get_queryset()
        return qs.filter(vizit__group__department=self.get_department()).distinct()


class RegisterListener(StudyGroupMixin, FormView):
    template_name = 'department/listener_register.html'
    form_class = ListenerAddForm

    def get_form(self, form_class):
        return form_class(self.get_studygroup(), **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.get_studygroup().get_absolute_url()


class StudyGroupListenersList(StudyGroupMixin, ListExtras, ListView):

    model = Listener
    template_name = 'department/studygroup_listener_list.html'
    filters = ['organization__name', 'position']
    search_fields = ['last_name__contains']

    def get_queryset(self):
        queryset = super(StudyGroupListenersList, self).get_queryset()
        return queryset.filter(group=self.get_studygroup())


class ListenerBatchSelect(StudyGroupListenersList):

    template_name = 'department/listener_add.html'

    def get_queryset(self):
        # все слушатели этого филиала
        return self.get_studygroup().department.listeners().filter(self.build_query())


class ListenerBatchApply(StudyGroupMixin, FormView):

    form_class = BatchListenersForm
    template_name = 'department/listener_add.html'

    def form_valid(self, form):
        studygroup = self.get_studygroup()
        if studygroup.status != enums.StudyGroupStatus.Pending:
            messages.add_message(self.request, messages.ERROR, u'В эту группу уже нельзя добавлять слушателей')
            return HttpResponseRedirect(reverse("department:studygroup_detail", kwargs={
                'department_id': self.get_department().pk,
                'pk': studygroup.pk
            }))

        for listener in form.cleaned_data['listeners']:
            listener.apply_studygroup(studygroup)

        if form.cleaned_data['listeners'].count() < 10:
            for listener in form.cleaned_data['listeners']:
                messages.add_message(self.request, messages.INFO, u'Добавлен слушатель %s' % listener)
        else:
            messages.add_message(self.request, messages.INFO, u'Добавлено %s слушателей' %
                                                              form.cleaned_data['listeners'].count())

        if 'next' in self.request.POST:
            return HttpResponseRedirect(self.request.POST['next'])
        else:
            return HttpResponseRedirect(reverse("department:studygroup_detail", kwargs={
                'department_id': self.get_department().pk,
                'pk': studygroup.pk
            }))

    def form_invalid(self, form):
        context = self.get_context_data()
        context.update({
            'form': form,
        })

        return self.render_to_response(context)


class ListenerAttestation(StudyGroupMixin, ListView):
    template_name = 'department/stugygroup_listener_attestation.html'
    fields = ['attestation_work_name']
    model = Vizit
    paginate_by = 5

    def get_queryset(self):
        return self.get_studygroup().vizit_set.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if 'is_paginated' in context and context['is_paginated']:
            page = context['page_obj']
            context['formset'] = self.construct_formset()(queryset=page.object_list)
        else:
            context['formset'] = self.construct_formset()(queryset=self.get_queryset())
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if 'is_paginated' in context and context['is_paginated']:
            page = context['page_obj']
            formset = self.construct_formset()(request.POST, queryset=page.object_list)
        else:
            formset = self.construct_formset()(request.POST, queryset=self.get_queryset())

        if formset.is_valid():
            formset.save()
        else:
            context['formset'] = formset
            print 'not valid!', formset.errors

            return self.render_to_response(context)


        if 'next_page' in request.POST:
            return HttpResponseRedirect(reverse('department:studygroup_listener_attestation',
                args=[self.get_department().pk, self.get_studygroup().pk]) + '?page=' + request.POST['next_page'])
        else:
            return HttpResponseRedirect(reverse('department:studygroup_detail',
                args=[self.get_department().pk, self.get_studygroup().pk]))


    def construct_formset(self):
        return modelformset_factory(self.model, fields=self.fields, extra=0)


class OrganizationList(DepartmentMixin, ListView):
    model = Organization
    template_name = 'department/organization_list.html'

    def get_queryset(self):
        return self.get_department().organizations()


class OrganizationDetail(DepartmentMixin, DetailView):
    model = Organization
    template_name = 'department/organization_detail.html'
