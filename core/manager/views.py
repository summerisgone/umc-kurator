# coding=utf-8
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView, View
from django.views.generic.detail import SingleObjectMixin
from core import enums
from core.enums import StudyGroupStatus
from core.manager.forms import StudyGroupCreateForm
from core.models import StudyGroup, update_group_numbers, Department
from crud.views import ListExtras
from utils import ExtraContextMixin, get_hours_data
from djappypod.response import OdtTemplateResponse


class SecurityMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'auth.' + enums.ADMINISTRATOR_PERMISSION[0]


class Index(SecurityMixin, ExtraContextMixin, TemplateView):
    template_name = 'manager/index.html'

    def extra_context(self):
        return {
            'groups': StudyGroup.objects.filter(status__in=[StudyGroupStatus.Pending, StudyGroupStatus.Certificated])[:10]
        }


class StudyGroupList(SecurityMixin, ExtraContextMixin, ListExtras, ListView):
    template_name = 'manager/studygroup_list.html'
    context_object_name = 'groups'
    model = StudyGroup
    filters = (
        'department',
        'status'
    )

    def extra_context(self):
        return {
            'department_list': Department.objects.all(),
            'group_statuses': enums.STUDY_GROUP_STATUSES,
        }


class StudyGroupRead(SecurityMixin, ExtraContextMixin, DetailView):
    template_name = 'manager/studygroup_detail.html'
    context_object_name = 'studygroup'
    pk_url_kwarg = 'stugygroup_id'
    model = StudyGroup


class StudyGroupDelete(SecurityMixin, DeleteView):
    template_name = 'manager/studygroup_confirm_delete.html'
    pk_url_kwarg = 'stugygroup_id'
    model = StudyGroup

    def get_success_url(self):
        messages.add_message(self.request, messages.WARNING, u'Группа удалена')
        return reverse('manager:group_list')


class StudyGroupCreate(SecurityMixin, ExtraContextMixin, CreateView):
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


class AutoNumerate(SecurityMixin, View):

    def post(self, request, *args, **kwds):
        groups = update_group_numbers()
        messages.add_message(self.request, messages.INFO,
             u'Автонумерация групп: ' + ','.join(
                 [g.subject.short_name + '-'  + g.subject.hours for g in groups])
        )
        return HttpResponseRedirect(reverse('manager:group_list'))


class StudyGroupClose(SecurityMixin, SingleObjectMixin, TemplateView):
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
            # Сначала выдать сертификаты, потом закрыть
            group.issue_certificates()
            group.status = enums.StudyGroupStatus.Closed
            group.save()
            messages.add_message(self.request, messages.INFO, u'Группа закрыта')
            return HttpResponseRedirect(reverse('manager:group_detail', args=[group.id,]))

        else:
            messages.add_message(self.request, messages.ERROR, u'Нельзя закрыть эту группу')
            return HttpResponseRedirect(reverse('manager:group_list'))


class GenerateCertificateList(SecurityMixin, ExtraContextMixin, DetailView):
    response_class = OdtTemplateResponse
    template_name = 'manager/certificates.odt'

    pk_url_kwarg = 'stugygroup_id'
    model = StudyGroup

    def extra_context(self):
        group = self.get_object()
        return {
            'group': group,
            'start': group.start,
            'end': group.end,
            'certificates': group.certificate_set.all(),
        }
