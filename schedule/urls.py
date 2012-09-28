# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from schedule.crud.models import crud

crud.register('core.Course')
crud.register('core.Subject')
crud.register('core.Department')
crud.register('auth.Teacher')

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('schedule.core.urls')),
    (r'^crud/', include('schedule.crud.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += staticfiles_urlpatterns()