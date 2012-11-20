# coding=utf-8
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.views.generic import TemplateView, DetailView, FormView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from core import enums
from core.enums import StudyGroupStatus
from core.manager.forms import StudyGroupCreateForm
from core.models import StudyGroup, update_group_numbers
from utils import ExtraContextMixin, get_hours_data


class Index(ExtraContextMixin, TemplateView):
    template_name = 'manager/index.html'

    def extra_context(self):
        return {
            'groups': StudyGroup.objects.all()[:10]
        }


class StudyGroupList(ExtraContextMixin, ListView):
    template_name = 'manager/studygroup_list.html'
    context_object_name = 'groups'
    model = StudyGroup


class StudyGroupRead(ExtraContextMixin, DetailView):
    template_name = 'manager/studygroup_detail.html'
    context_object_name = 'studygroup'
    pk_url_kwarg = 'stugygroup_id'
    model = StudyGroup


class StudyGroupDelete(DeleteView):
    template_name = 'manager/studygroup_confirm_delete.html'
    pk_url_kwarg = 'stugygroup_id'
    model = StudyGroup

    def get_success_url(self):
        messages.add_message(self.request, messages.WARNING, u'Группа удалена')
        return reverse('manager:group_list')

class StudyGroupCreate(ExtraContextMixin, CreateView):
    form_class = StudyGroupCreateForm
    model = StudyGroup
    template_name = 'manager/studygroup_form.html'

    def get_success_url(self):
        return reverse('manager:group_list')

    def extra_context(self):
        return {
            'hours': simplejson.dumps(get_hours_data())
        }

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class StudyGroupUpdate(StudyGroupCreate, UpdateView):
    queryset = StudyGroup.objects.filter(status=StudyGroupStatus.Pending)
    pk_url_kwarg = 'stugygroup_id'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


def update_numbers(request):
    update_group_numbers()
    return HttpResponseRedirect(reverse('manager:group_list'))


class StudyGroupClose(SingleObjectMixin, TemplateView):
    model = StudyGroup
    template_name = 'manager/studygroup_confirm_close.html'
    pk_url_kwarg = 'stugygroup_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        group = self.get_object()
        if group.is_last_attestated():
            group.status = enums.StudyGroupStatus.Closed
            group.save()
            messages.add_message(self.request, messages.INFO, u'Группа закрыта')
        else:
            messages.add_message(self.request, messages.ERROR, u'Нельзя закрыть эту группу')
        return HttpResponseRedirect(reverse('manager:group_list'))
