from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from .views import HomeView
from .views import CategoryDetailView
from .views import ArticleDetailView
from .views import SearchResultsListView


admin.site.site_title = 'Knowledge Base'
admin.site.site_header = 'Knowledge Base'


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name='home'),

    url(
        r'^categoria/(?P<slug>[\w\-]+)/$',
        CategoryDetailView.as_view(),
        name='category_detail'
    ),

    url(
        r'^articulo/(?P<slug>[\w\-]+)/$',
        ArticleDetailView.as_view(),
        name='article_detail'
    ),

    url(
        r'^search/$',
        SearchResultsListView.as_view(),
        name='search_results_list'
    ),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
