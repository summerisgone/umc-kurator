# coding=utf-8
from django.views.generic import TemplateView, FormView
from auth.models import Listener
from core.models import Course
from reports.forms import ReportQueryForm
from reports.query import ResultTable, PARAMETERS


class ReportList(TemplateView):
    template_name = 'reports/index.html'


class ListenersCount(FormView):
    template_name = 'reports/listeners_count.html'
    form_class = ReportQueryForm

    def form_valid(self, form):
        cols = PARAMETERS[form.cleaned_data['vertical']]()
        rows = PARAMETERS[form.cleaned_data['horizontal']]()
        rt = ResultTable(rows, cols, Listener.objects.all())
        return self.render_to_response({
            'table': rt,
            'data': rt.process(),
            'form': form,
        })
