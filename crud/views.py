# -*- coding: utf-8 -*-
from django.db.models import Q

class ListExtras:
    """
    Usage:

    class ArticleList(ListExtras, ListView):

        model = Article

        # add form with ``author__id`` and ``status`` fields to filter results
        filters = [{'request': 'author', 'query': 'author__id'}, 'status']

        # add form with ``input[name=search]`` to search results by text
        search_fields = ['text__contains']

    """

    filters = []
    search_fields = []
    paginate_by = 50
    # model = MyModel()

    def build_filter(self, query):
        for filter in self.filters:
            if isinstance(filter, str):
                if filter in self.request.REQUEST and self.request.REQUEST[filter]:
                    query &= Q(**{
                        filter: self.request.REQUEST[filter]
                    })
            elif isinstance(filter, dict):
                assert ('request' in filter, 'query' in filter)
                if filter['request'] in self.request.REQUEST and self.request.REQUEST[filter['request']]:
                    query &= Q(**{
                        filter['query']: self.request.REQUEST[filter['request']]
                    })
        return query

    def build_search(self, query):
        if 'search' in self.request.REQUEST and self.request.REQUEST['search']:
            for search_field in self.search_fields:
                query &= Q(**{
                    search_field: self.request.REQUEST['search']
                })
        return query

    def build_query(self):
        query = Q()
        query = self.build_filter(query)
        query = self.build_search(query)
        return query

    def get_queryset(self):
        return self.model.objects.filter(self.build_query())
