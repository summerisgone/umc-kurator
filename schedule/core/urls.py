# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from schedule.core.views import DepartmentList, DepartmentDetail, CourseDetail, AddListener

urlpatterns = patterns('',
    url(r'^$', DepartmentList.as_view(), name='department_list'),
    url(r'^dep/(?P<pk>\d{1,5})/$', DepartmentDetail.as_view(), name='department_detail'),
    url(r'^dep/courses/(?P<pk>\d{1,5})/$', CourseDetail.as_view(), name='course_detail'),
    url(r'^dep/courses/(?P<course_pk>\d{1,5})/add_listener/$', AddListener.as_view(), name='add_listener'),
)