# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import Index, StudyGroupList, StudyGroupCreate, StudyGroupRead

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    url(r'^sg/$', StudyGroupList.as_view(), name='group_list'),
    url(r'^sg/add/$', StudyGroupCreate.as_view(), name='group_add'),
    url(r'^sg/(?P<stugygroup_id>\d{1,5})/$', StudyGroupRead.as_view(), name='group_detail'),
#    url(r'^sg/(?P<stugygroup_id>\d{1,5})/delete/$', StudyGroupRead.as_view(), name='group_detail'),
)
