# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import Index


urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='frontpage'),
    url(r'^', include('core.department.urls', namespace='department')),
    url(r'^manage/', include('core.manager.urls', namespace='manager')),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
)
