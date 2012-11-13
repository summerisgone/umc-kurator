# -*- coding: utf-8 -*-
from django.db.models import Q

class ListExtras:
    """
    Usage:

    class ArticleList(ListExtras, ListView):

        model = Article

        # add form with ``author__id`` and ``genre__id`` fields to filter results
        filters = ['author__id', 'genre__id']

        # add form with ``input[name=search]`` to search results by text
        search_fields = ['text__contains']

    """

    filters = []
    search_fields = []
    paginate_by = 50
    # model = MyModel()

    def build_query(self):
        query = Q()
        for filter in self.filters:
            if filter in self.request.REQUEST and self.request.REQUEST[filter]:
                query &= Q(**{
                    filter: self.request.REQUEST[filter]
                })
        if 'search' in self.request.REQUEST and self.request.REQUEST['search']:
            for search_field in self.search_fields:
                query &= Q(**{
                    search_field: self.request.REQUEST['search']
                })
        return query

    def get_queryset(self):
        return self.model.objects.filter(self.build_query())
