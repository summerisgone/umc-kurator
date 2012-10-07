# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from schedule.core.views import AddListener, CourseAdd, Index, EmitCertificate, ListenersList


urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^dep-(?P<department_id>\d{1,5})/course/add/$', CourseAdd.as_view(), name='course_add'),
    url(r'^course/(?P<course_pk>\d{1,5})/register/$', AddListener.as_view(), name='add_listener'),
    url(r'^course/(?P<course_pk>\d{1,5})/listeners/$', ListenersList.as_view(),
        name='course_listeners_list'),
    url(r'^cert/(?P<course_id>\d{1,5})-(?P<listener_id>\d{1,5})/$', EmitCertificate.as_view(),
        name='emit_certificate'),
)
