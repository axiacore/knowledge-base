from django.contrib.postgres.search import SearchVector
from django.db.models import F
from django.views.generic import ListView
from django.views.generic import DetailView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Category
from .models import Article
from .forms import SearchForm


class HomeView(ListView):
    template_name = 'home.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


class CategoryDetailView(DetailView):
    model = Category


class ArticleDetailView(DetailView):
    model = Article


class SearchResultsListView(ListView):
    model = Article
    template_name = 'app/search_results_list.html'

    def get_queryset(self):
        search = self.request.GET.get('text', '')
        return Article.objects.annotate(
            search=SearchVector(
                'content',
                'name'
                )
            ).filter(
            search=search
        )

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


class ArticleUpVoteView(DetailView):

    model = Article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if request.session.get('voted_article_list'):
            voted_list = request.session.get('voted_article_list', [])
        else:
            voted_list = []

        if article.id not in voted_list:
            voted_list.append(article.id)
            request.session['voted_article_list'] = voted_list
            article.upvotes = F('upvotes') + 1
            article.save()
            article = self.get_object()
        votes = article.upvotes
        data = [
            {
                'upvotes': votes
            }
        ]
        return JsonResponse(data, safe=False)


class ArticleDownVoteView(DetailView):

    model = Article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if request.session.get('voted_article_list'):
            voted_list = request.session.get('voted_article_list', [])
        else:
            voted_list = []

        if article.id not in voted_list:
            voted_list.append(article.id)
            request.session['voted_article_list'] = voted_list
            article.downvotes = F('downvotes') + 1
            article.save()
            article = self.get_object()
        votes = article.downvotes
        data = [
            {
                'downvotes': votes
            }
        ]
        return JsonResponse(data)
