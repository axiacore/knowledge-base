from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.translation import ugettext as _

from .views import HomeView
from .views import CategoryDetailView
from .views import ArticleDetailView
from .views import SearchResultsListView
from .views import ArticleUpVoteView
from .views import ArticleDownVoteView


admin.site.site_title = 'Knowledge Base'
admin.site.site_header = 'Knowledge Base'


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name='home'),

    url(
        r'^{0}/(?P<slug>[\w\-]+)/$'.format(
            _('category')
        ),
        CategoryDetailView.as_view(),
        name='category_detail'
    ),

    url(
        r'^(?P<category_slug>[\w\-]+)/(?P<slug>[\w\-]+)/$',
        ArticleDetailView.as_view(),
        name='article_detail'
    ),

    url(
        r'^(?P<category_slug>[\w\-]+)/(?P<slug>[\w\-]+)/upvote/$',
        ArticleUpVoteView.as_view(),
        name='article_upvote'
    ),

    url(
        r'^(?P<category_slug>[\w\-]+)/(?P<slug>[\w\-]+)/downvote/$',
        ArticleDownVoteView.as_view(),
        name='article_downvote'
    ),

    url(
        r'^{0}/$'.format(_('search')),
        SearchResultsListView.as_view(),
        name='search_results_list'
    ),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
