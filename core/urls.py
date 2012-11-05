# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from views import Index


urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='frontpage'),
    url(r'^', include('department.urls',
        namespace='department')),
)