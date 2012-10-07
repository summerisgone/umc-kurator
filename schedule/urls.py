# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from schedule.crud.models import crud

crud.register('core.Course')
crud.register('core.Subject')
crud.register('core.Department')
crud.register('core.Organization')
crud.register('auth.Teacher')
crud.register('auth.Listener')

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('schedule.core.urls')),
    (r'^reports/', include('schedule.reports.urls')),
    (r'^crud/', include('schedule.crud.urls', namespace='crud')),
    (r'^api/', include('schedule.api.urls', namespace='api')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('djangorestframework.urls', namespace='djangorestframework'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += staticfiles_urlpatterns()