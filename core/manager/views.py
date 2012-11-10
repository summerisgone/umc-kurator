# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, FormView, ListView
from core.manager.forms import StudyGroupCreateForm
from core.models import StudyGroup
from utils import ExtraContextMixin


class Index(TemplateView):
    template_name = 'manager/index.html'


class StudyGroupList(ExtraContextMixin, ListView):
    template_name = 'manager/study_group_list.html'
    context_object_name = 'groups'
    model = StudyGroup


class StudyGroupRead(ExtraContextMixin, DetailView):
    template_name = 'manager/study_group_detail.html'
    context_object_name = 'studygroup'
    model = StudyGroup


class StudyGroupCreate(ExtraContextMixin, FormView):
    form_class = StudyGroupCreateForm
    template_name = 'manager/study_group_add.html'

    def get_success_url(self):
        return reverse('manager:manager_index')

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())