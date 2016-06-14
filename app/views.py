from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Category
from .models import Article
from .forms import SearchForm


class HomeView(ListView):
    template_name = 'home.html'
    model = Category
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'


class SearchResultsListView(ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context
