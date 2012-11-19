# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import RegisterListener, StudyGroupList, StudyGroupDetail,\
    OrganizationList, StudyGroupListenersList, ListenerAddBatch, \
    ListenerList, OrganizationDetail, Index, StudyGroupComplete, ListenerAttestation


urlpatterns = patterns('',
    url(r'^d(?P<department_id>\d{1,5})/$', Index.as_view(), name='index'),

    url(r'^d(?P<department_id>\d{1,5})/groups/$', StudyGroupList.as_view(), name='studygroup_list'),
    url(r'^d(?P<department_id>\d{1,5})/listeners/$', ListenerList.as_view(), name='listener_list'),
    url(r'^d(?P<department_id>\d{1,5})/organizations/$', OrganizationList.as_view(),
        name='organization_list'),

    # studygroup-related  urls

    url(r'^d(?P<department_id>\d{1,5})/group/(?P<pk>\d{1,5})/$', StudyGroupDetail.as_view(),
        name='studygroup_detail'),
    url(r'^d(?P<department_id>\d{1,5})/group/(?P<pk>\d{1,5})/complete/$', StudyGroupComplete.as_view(),
            name='studygroup_complete'),
    url(r'^d(?P<department_id>\d{1,5})/group/(?P<studygroup_pk>\d{1,5})/listeners/$',
        StudyGroupListenersList.as_view(), name='studygroup_listeners_list'),
    url(r'^d(?P<department_id>\d{1,5})/group/(?P<studygroup_pk>\d{1,5})/listeners/add/$',
        ListenerAddBatch.as_view(), name='studygroup_listener_add'),
    url(r'^d(?P<department_id>\d{1,5})/group/(?P<studygroup_pk>\d{1,5})/listeners/attestation/$',
        ListenerAttestation.as_view(),
        name='studygroup_listener_attestation'),
    url(r'^d(?P<department_id>\d{1,5})/group/(?P<studygroup_pk>\d{1,5})/register/$',
        RegisterListener.as_view(), name='studygroup_listener_register'),

    # Organization

    url(r'^d(?P<department_id>\d{1,5})/organization/(?P<pk>\d{1,5})/$', OrganizationDetail.as_view(),
            name='organization_detail'),


    # url(r'^d(?P<department_id>\d{1,5})/cert/(?P<studygroup_pk>\d{1,5})-(?P<listener_id>\d{1,5})/$',
    #    EmitCertificate.as_view(), name='emit_certificate'),
)
