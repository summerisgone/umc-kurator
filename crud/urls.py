# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from models import crud

urlpatterns = crud.get_urlconf()