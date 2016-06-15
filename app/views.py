from django.contrib.postgres.search import SearchVector
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Category
from .models import Article
from .forms import SearchForm


class HomeView(ListView):
    template_name = 'home.html'
    model = Article

    def get_queryset(self):
        """ Return a queryset based on whether the
            user is authenticated or not.
        """
        if self.request.user.is_authenticated():
            return Article.active.all()
        return Article.public.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


class CategoryDetailView(DetailView):
    model = Category


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self):
        return get_object_or_404(
            Article,
            slug=self.kwargs['slug'],
            category__slug=self.kwargs['category_slug'],
        )


class SearchResultsListView(ListView):
    model = Article
    template_name = 'app/search_results_list.html'

    def get_queryset(self):
        search = self.request.GET.get('text', '')
        return Article.objects.annotate(
            search=SearchVector(
                'content',
                'name',
                config=settings.SEARCH_LANGS[
                    settings.LANGUAGE
                ]
            )
        ).filter(
            search=search
        )

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context
