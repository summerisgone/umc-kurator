# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import Index, StudyGroupList, StudyGroupCreate, StudyGroupRead, StudyGroupUpdate, \
    StudyGroupDelete, update_numbers, StudyGroupClose, GenerateCertificateList

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^sg/$', StudyGroupList.as_view(), name='group_list'),
    url(r'^sg/autonum/$', update_numbers, name='update_numers'),
    url(r'^sg/add/$', StudyGroupCreate.as_view(), name='group_add'),
    url(r'^sg/(?P<stugygroup_id>\d{1,5})/$', StudyGroupRead.as_view(), name='group_detail'),
    url(r'^sg/(?P<stugygroup_id>\d{1,5})/edit/$', StudyGroupUpdate.as_view(), name='group_edit'),
    url(r'^sg/(?P<stugygroup_id>\d{1,5})/delete/$', StudyGroupDelete.as_view(), name='group_delete'),
    url(r'^sg/(?P<stugygroup_id>\d{1,5})/close/$', StudyGroupClose.as_view(), name='group_close'),
    url(r'^sg/(?P<stugygroup_id>\d{1,5})/certificates.odt$', GenerateCertificateList.as_view(), name='group_detail'),
)
