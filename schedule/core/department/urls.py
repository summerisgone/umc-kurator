# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView
from core.models import Department
from views import AddListener, CourseAdd, CourseList, CourseDetail,\
    EmitCertificate, CourseListenersList, ListenerBatchSelect, ListenerBatchUpdate


urlpatterns = patterns('',
    url(r'^d(?P<pk>\d{1,5})/$', DetailView.as_view(model=Department,
        template_name='department/department_detail.html',
        context_object_name='department'),
        name='index'),

    # course-related  urls

    url(r'^d(?P<department_id>\d{1,5})/course/$', CourseList.as_view(), name='course_list'),
    url(r'^d(?P<department_id>\d{1,5})/course/add/$', CourseAdd.as_view(), name='course_add'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<pk>\d{1,5})/$', CourseDetail.as_view(),
        name='course_detail'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<course_pk>\d{1,5})/listeners/$',
        CourseListenersList.as_view(), name='course_listeners_list'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<course_pk>\d{1,5})/register/$',
        AddListener.as_view(), name='course_listener_add'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<course_pk>\d{1,5})/select_batch/$',
        ListenerBatchSelect.as_view(), name='course_listener_add_batch'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<course_pk>\d{1,5})/register_batch/$',
        ListenerBatchUpdate.as_view(),
        name='course_listener_update_batch'),

    # url(r'^d(?P<department_id>\d{1,5})/cert/(?P<course_pk>\d{1,5})-(?P<listener_id>\d{1,5})/$',
    #    EmitCertificate.as_view(), name='emit_certificate'),
)
