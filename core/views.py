# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from core.models import Department

class Index(TemplateView):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('auth.is_admin') and not request.user.is_staff:
            return HttpResponseRedirect(reverse('manager:index'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return {
            'departments': Department.objects.all(),
        }
