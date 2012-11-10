# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from djangorestframework.views import ListOrCreateModelView
from core.api.resources import AutoCompleteLastName, AutoCompletePatronymic, \
    AutoCompleteFirstName, \
    AutoCompeteUser, AutoCompleteOrganization, OrganizationResource


urlpatterns = patterns('',
    url(r'^autocomplete/last_name/$', AutoCompleteLastName.as_view(),
        name='autocomplete_last_name'),
    url(r'^autocomplete/first_name/$', AutoCompleteFirstName.as_view(),
        name='autocomplete_first_name'),
    url(r'^autocomplete/patronymic/$', AutoCompletePatronymic.as_view(),
        name='autocomplete_patronymic'),
    url(r'^autocomplete/organization/$', AutoCompleteOrganization.as_view(),
            name='autocomplete_organization'),
    url(r'^autocomplete/user/$', AutoCompeteUser.as_view(),
        name='autocomplete_user'),
    url(r'^organization/', ListOrCreateModelView.as_view(resource=OrganizationResource),
        name='organization')
)
