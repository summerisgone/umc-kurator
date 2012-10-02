# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from reports.views import ReportList, ListenersCount


urlpatterns = patterns('',
    url(r'^$', ReportList.as_view(), name='report_index'),
    url(r'^count/$', ListenersCount.as_view(), name='listeners_count'),
)
