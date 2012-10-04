# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from api.resources import AutocompleteLastName


urlpatterns = patterns('',
    url(r'^autocomplete/last_name/$', AutocompleteLastName.as_view(),
        name='autocomplete_lastname'),
)
