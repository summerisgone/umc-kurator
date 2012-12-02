# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from reports.views import ReportWizard, ReportDetail, ReportList, ReportByDepartment, ReportBySubject


urlpatterns = patterns('',
    url(r'^$', ReportList.as_view(), name='report_index'),
    url(r'^by_department/$', ReportByDepartment.as_view(), name='report_by_department'),
    url(r'^by_subject/$', ReportBySubject.as_view(), name='report_by_subject'),
    url(r'^wizard/$', ReportWizard.as_view(), name='report_wizard'),
    url(r'^(?P<pk>\d{1,5})$', ReportDetail.as_view(), name='report_detail'),
)
