# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView
from core.models import Department
from views import AddListener, CourseAdd, CourseList, CourseDetail,\
    OrganizationList, CourseListenersList, ListenerBatchSelect, \
    ListenerBatchApply, ListenerList, OrganizationDetail


urlpatterns = patterns('',
    url(r'^d(?P<pk>\d{1,5})/$', DetailView.as_view(model=Department,
        template_name='department/department_detail.html',
        context_object_name='department'),
        name='index'),

    url(r'^d(?P<department_id>\d{1,5})/course/$', CourseList.as_view(), name='course_list'),
    url(r'^d(?P<department_id>\d{1,5})/listeners/$', ListenerList.as_view(), name='listener_list'),
    url(r'^d(?P<department_id>\d{1,5})/organizations/$', OrganizationList.as_view(),
        name='organization_list'),

    # course-related  urls

    url(r'^d(?P<department_id>\d{1,5})/course/add/$', CourseAdd.as_view(), name='course_add'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<pk>\d{1,5})/$', CourseDetail.as_view(),
        name='course_detail'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<course_pk>\d{1,5})/listeners/$',
        CourseListenersList.as_view(), name='course_listeners_list'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<course_pk>\d{1,5})/register/$',
        AddListener.as_view(), name='course_listener_add'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<course_pk>\d{1,5})/add_batch/$',
        ListenerBatchSelect.as_view(), name='course_listener_add_batch'),
    url(r'^d(?P<department_id>\d{1,5})/course/(?P<course_pk>\d{1,5})/update_batch/$',
        ListenerBatchApply.as_view(),
        name='course_listener_apply_batch'),

    # Organization

    url(r'^d(?P<department_id>\d{1,5})/organization/(?P<pk>\d{1,5})/$', OrganizationDetail.as_view(),
            name='organization_detail'),


    # url(r'^d(?P<department_id>\d{1,5})/cert/(?P<course_pk>\d{1,5})-(?P<listener_id>\d{1,5})/$',
    #    EmitCertificate.as_view(), name='emit_certificate'),
)
