# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from schedule.core.views import DepartmentList, DepartmentDetail

urlpatterns = patterns('',
    url(r'^$', DepartmentList.as_view(), name='department_list'),
    url(r'^dep/(?P<pk>\d{1,5})$', DepartmentDetail.as_view(), name='department_detail'),
)