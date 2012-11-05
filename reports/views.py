# coding=utf-8
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.views.generic import TemplateView, FormView, DetailView
from django.template.loader import render_to_string
from datetime import datetime
from reports.forms import ReportQueryForm
from reports.models import Report, ReportStatus


class ReportList(TemplateView):
    template_name = 'reports/index.html'


class ReportDetail(DetailView):
    model = Report

    def get_context_data(self, **kwargs):
        context = super(ReportDetail, self).get_context_data(**kwargs)
        if self.object.status == ReportStatus.Ready:
            context.update({
                'report_html': render_to_string(self.object.template_name,
                    simplejson.loads(self.object.data)),
            })
        return context


class ListenersCount(FormView):
    template_name = 'reports/listeners_count.html'
    form_class = ReportQueryForm

    def form_valid(self, form):

        reports = Report.objects.filter(
            vertical=form.cleaned_data['vertical'],
            horizontal=form.cleaned_data['horizontal'],
        )

        if reports.filter(status=ReportStatus.Ready).exists():
            report = reports.filter(status=ReportStatus.Ready)[0]

            return HttpResponseRedirect(report.get_absolute_url())
        elif reports.exists():
            return self.render_to_response({
                'form': form,
                'pending': reports[0]
            })
        else:
            report = Report(
                vertical=form.cleaned_data['vertical'],
                horizontal=form.cleaned_data['horizontal'],
                status=ReportStatus.Pending,
                template_name='reports/default.html',
                year=datetime.today().year
            )
            report.save()
            report.process.delay()
            return self.render_to_response({'form': form, 'created': report})
