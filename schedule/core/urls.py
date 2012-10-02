# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from schedule.core.views import AddListener, CourseAdd, Index, EmitCertificate


urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^dep-(?P<department_id>\d{1,5})/course/add/$', CourseAdd.as_view(), name='course_add'),
    url(r'^register/(?P<course_pk>\d{1,5})/$', AddListener.as_view(), name='add_listener'),
    url(r'^cert/(?P<course_id>\d{1,5})-(?P<listener_id>\d{1,5})/$', EmitCertificate.as_view(),
        name='emit_certificate'),
)
