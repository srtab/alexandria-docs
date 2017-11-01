# -*- coding: utf-8 -*-
from django.views.generic.list import ListView

from haystack.inputs import Clean
from haystack.query import SQ, SearchQuerySet
from projects.models import ImportedFile, Project


class SearchView(ListView):
    """ """
    template_name = "search/index.html"
    search_model = None
    search_field = 'q'
    paginate_by = 20

    def get_query(self):
        return self.request.GET.get(self.search_field, "")

    def get_queryset(self):
        return self.search(self.get_query()).models(self.search_model)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        queryset = self.search(self.get_query())
        context.update({
            'query': self.get_query(),
            'projects_count': queryset.models(Project).count(),
            'pages_count': queryset.models(ImportedFile).count()
        })
        return context

    def search(self, query):
        return SearchQuerySet().filter(visibility_level=Project.Level.PUBLIC)\
            .filter(SQ(content__contains=Clean(query)) |
                    SQ(title__contains=Clean(query)))


class SearchProjectView(SearchView):
    """ """
    search_model = Project


class SearchPageView(SearchView):
    """ """
    search_model = ImportedFile
