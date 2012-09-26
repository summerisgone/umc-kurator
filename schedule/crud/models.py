# coding=utf-8
from django.core.urlresolvers import reverse
from django.db.models import loading
from django.utils.decorators import classonlymethod
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.conf.urls.defaults import patterns, include, url

class Action(object):
    List = 'list'
    Create = 'create'
    Read = 'read'
    Update = 'update'
    Delete = 'delete'

ACTIONS = (Action.List, Action.Create, Action.Read, Action.Update, Action.Delete)

class Registry(dict):

    def __init__(self, model):
        self.model = model
        super(dict, self).__init__()

    def __getattr__(self, action):
        if action in ACTIONS:
            return self[action]
        getattr(self, action)


    def __setattr__(self, action, value):
        if action in ACTIONS:
            self[action] = value
        return super(Registry, self).__setattr__(action, value)

class Crud(object):

    def __init__(self):
        self._registry = {}

    def get_action_view(self, model_str, action):
        app_label, model_name = model_str.split('.')
        modelCls = loading.get_model(app_label, model_name)
        baseCls = self.get_base_class_for_action(action)

        class ViewClass(baseCls):
            model = modelCls
            if action == Action.Delete:
                success_url = '../../'
            else:
                success_url = '../'
            template_name = 'crud/object_%s.html' % action

            def get_template_names(self):
                names = super(ViewClass, self).get_template_names()
                # push crud template down to last default
                names[0], names[-1] = names[-1], names[0]
                return names

        return ViewClass

    def register(self, model_str, action=None, view=None):
        if model_str not in self._registry:
            self._registry[model_str] = Registry(model_str)

        if action and view:
            self._registry[model_str][action] = view

    def get_urlconf(self):
        url_patterns = patterns('', )
        for model_str, model_registry in self._registry.iteritems():
            app_label, model_name = model_str.split('.')
            for action in ACTIONS:
                regexp = self.get_url_regexp_for_action(action) % (app_label, model_name.lower())
                url_kwargs = {'namespace': 'crud'}
                url_name = '%s.%s.%s' % (app_label, model_name.lower(), action)
                if action in model_registry:

                    # TODO: сделать поддержку обычных вьюх
                    url_patterns += patterns('',
                        url(regexp, model_registry[action].as_view(),
                            kwargs=url_kwargs, name=url_name),
                    )
                else:
                    url_patterns += patterns('',
                        url(regexp, self.get_action_view(model_str, action).as_view(),
                            kwargs=url_kwargs, name=url_name),
                    )
        return url_patterns

    def get_base_class_for_action(self, action):
        if action == Action.List:
            return ListView
        elif action == Action.Create:
            return CreateView
        elif action == Action.Read:
            return DetailView
        elif action == Action.Update:
            return UpdateView
        elif action == Action.Delete:
            return DeleteView

    def get_url_regexp_for_action(self, action):
        if action == Action.List:
            return r'^%s/%s/$'
        elif action == Action.Create:
            return r'^%s/%s/add/$'
        elif action == Action.Read:
            return r'^%s/%s/(?P<pk>\d{1,5})/$'
        elif action == Action.Update:
            return r'^%s/%s/(?P<pk>\d{1,5})/edit/$'
        elif action == Action.Delete:
            return r'^%s/%s/(?P<pk>\d{1,5})/delete/$'


crud = Crud()
