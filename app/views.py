from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Category
from .models import Article
from .forms import SearchForm


class HomeView(ListView):
    template_name = 'home.html'
    model = Category

    def get_queryset(self):
        """ Returns an empty queryset as we're sending the
            constructed data (category_list) in `get_context_data`.
        """
        return Category.objects.none()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        category_list = []
        category_slugs = Category.objects.filter(
            article__isnull=False,
        ).distinct()

        article_list = Article.objects.filter(
            is_active=True,
        )

        # Creates an iterable structure that can be used in templates.
        for category in category_slugs:
            category_articles = article_list.filter(
                category=category,
            )

            # If user is not authenticated, prevent
            # `private` articles from being shown.
            if not self.request.user.is_authenticated():
                category_articles = category_articles.filter(
                    is_private=False,
                )

            category_list.append([
                category.name,
                category.slug,
                category_articles,
            ])

        context.update({
            'category_list': category_list,
            'form': SearchForm()
        })
        return context


class CategoryDetailView(DetailView):
    model = Category


class ArticleDetailView(DetailView):
    model = Article


class SearchResultsListView(ListView):
    model = Article

    def get_queryset(self):
        search = self.request.GET.get('text', '')
        return Article.objects.filter(content__search=search)

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context
