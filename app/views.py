from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Category
from .models import Article


class HomeView(ListView):
    template_name = 'home.html'
    model = Category
    context_object_name = 'category_list'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
