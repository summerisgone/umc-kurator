# Create your views here.
from django.db.models import Q
from django.views.generic import ListView
from core.models import Organization
from schedule import enums
from models import Listener

class ListenersList(ListView):
    model = Listener
    paginate_by = 50

    def build_query(self):
        query = Q()
        if 'organization' in self.request.GET:
            try:
                org = Organization.objects.get(name=self.request.GET['organization'])
                query &= Q(organization=org)
            except Organization.DoesNotExist:
                pass
        if 'position' in self.request.GET and \
            self.request.GET['position'] in [pos[1] for pos in enums.LISTENER_POSITIONS]:
            query &= Q(position=self.request.GET['position'])
        return query

    def get_queryset(self):
        return self.model.objects.filter(self.build_query())

    def get_context_data(self, **kwargs):
        context = super(ListenersList, self).get_context_data(**kwargs)
        if hasattr(self, 'extra_context'):
            if callable(self.extra_context):
                context.update(self.extra_context())
            else:
                context.update(self.extra_context)

        return context
