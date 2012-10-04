# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from api.resources import AutoCompleteLastName, AutoCompletePatronymic, AutoCompleteFirstName


urlpatterns = patterns('',
    url(r'^autocomplete/last_name/$', AutoCompleteLastName.as_view(),
        name='autocomplete_last_name'),
    url(r'^autocomplete/first_name/$', AutoCompleteFirstName.as_view(),
        name='autocomplete_first_name'),
    url(r'^autocomplete/patronymic/$', AutoCompletePatronymic.as_view(),
        name='autocomplete_patronymic'),
)
