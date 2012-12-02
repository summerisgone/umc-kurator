# coding=utf-8
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.views.generic import TemplateView, FormView, DetailView
from django.template.loader import render_to_string
from librabbitmq import ConnectionError
from reports.forms import ReportQueryForm, DepartmentForm, SubjectForm
from reports.models import Report, ReportStatus


class BaseReportWizard(object):

    def form_valid(self, form):
        report_query = self.get_report_query(form)
        report_dict = self.get_report_dict(form)

        reports = Report.objects.filter(**report_query)

        if reports.filter(status=ReportStatus.Ready).exists():
            report = reports.filter(status=ReportStatus.Ready)[0]
        elif reports.filter(status=ReportStatus.Pending).exists():
            return self.render_to_response({
                'form': form,
                'pending': reports[0]
            })
        else:
            report = Report(**report_dict)
            report.save()
            try:
                report.process() #.delay(report)
            except ConnectionError:
                return self.render_to_response({
                    'form': form,
                    'error': u'Нет соединения с очередью задач'
                })
            return HttpResponseRedirect(report.get_absolute_url())

    def get_report_dict(self, form):
        report_query = self.get_report_query(form)
        report_dict = report_query.copy()
        report_dict.update({
            'status': ReportStatus.Pending,
            'template_name': 'reports/default.html',
        })
        return report_dict


class ReportList(TemplateView):
    template_name = 'reports/index.html'


class ReportByDepartment(BaseReportWizard, FormView):
    template_name = 'reports/report_by_department.html'
    form_class = DepartmentForm

    def get_report_query(self, form):
        report_query = {
            'horizontal': 'subject',
            'vertical': 'category',
            'grouping': 'time_range',
            'filter_name': 'group__department',
            'filter_value': form.cleaned_data['department']
        }
        return report_query


class ReportBySubject(BaseReportWizard, FormView):
    template_name = 'reports/report_by_subject.html'
    form_class = SubjectForm

    def get_report_query(self, form):
        report_query = {
            'horizontal': 'department',
            'vertical': 'category',
            'grouping': 'time_range',
            'filter_name': 'group__subject',
            'filter_value': form.cleaned_data['subject']
        }
        return report_query


class ReportWizard(BaseReportWizard, FormView):
    template_name = 'reports/report_wizard.html'
    form_class = ReportQueryForm

    def get_report_query(self, form):
        return {
            'vertical': form.cleaned_data['vertical'],
            'horizontal': form.cleaned_data['horizontal'],
            'grouping': form.cleaned_data['grouping']
        }


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
