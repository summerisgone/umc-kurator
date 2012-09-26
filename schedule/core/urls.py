# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from schedule.core.views import AddListener, CourseAdd, Index


urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^dep-(?P<department_id>\d{1,5})/course/add/$', CourseAdd.as_view(), name='course_add'),
    url(r'^dep/courses/(?P<course_pk>\d{1,5})/add_listener/$', AddListener.as_view(), name='add_listener'),
)
