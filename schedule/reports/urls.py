# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from reports.views import ReportList


urlpatterns = patterns('',
    url(r'^$', ReportList.as_view(), name='report_index'),
)
