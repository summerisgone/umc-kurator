# coding=utf-8
from django.views.generic import TemplateView
from auth.models import Listener
from core.models import Course
from reports.forms import ReportQueryForm


class ReportList(TemplateView):
    template_name = 'reports/index.html'


class ListenersCount(TemplateView):
    template_name = 'reports/listeners_count.html'

    def get(self, request, *args, **kwargs):
        form = ReportQueryForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = ReportQueryForm(request.POST)
        if form.is_valid():
            query = form.get_query()
            data = self.build_report(query)
            return self.render_to_response({
                'form': form,
                'report': data
            })
        else:
            return self.render_to_response({'form': form})

    def build_report(self, query):
        courses_ids = Course.objects.filter(query).values_list('id', flat=True)
        listeners = Listener.objects.filter(courses__id__in=courses_ids)
        return listeners