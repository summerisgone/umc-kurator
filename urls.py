# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('core.urls')),
    (r'^reports/', include('reports.urls')),
    (r'^api/', include('core.api.urls', namespace='api')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('djangorestframework.urls', namespace='djangorestframework'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += staticfiles_urlpatterns()