from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout
from django.utils.translation import ugettext_lazy as _

from .views import ArticleDetailView
from .views import ArticleDownVoteView
from .views import ArticleUpVoteView
from .views import CategoryDetailView
from .views import HomeView
from .views import LoginView
from .views import SearchResultsListView
from .views import ArticleDetailFeedbackView


admin.site.site_title = _('Knowledge Base')
admin.site.site_header = _('Knowledge Base')


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^markdownx/', include('markdownx.urls')),

    url(r'^robots\.txt$', include('robots.urls')),

    url(
        _(r'^search/$'),
        SearchResultsListView.as_view(),
        name='search_results_list'
    ),

    url(
        _(r'^login/$'),
        LoginView.as_view(),
        name='login'
    ),

    url(
        _(r'^logout/$'),
        logout,
        {'next_page': '/'},
        name='logout'
    ),

    url(r'^$', HomeView.as_view(), name='home'),

    url(
        r'^(?P<slug>[\w\-]+)/$',
        CategoryDetailView.as_view(),
        name='category_detail'
    ),

    url(
        r'^(?P<category_slug>[\w\-]+)/(?P<slug>[\w\-]+)/$',
        ArticleDetailView.as_view(),
        name='article_detail'
    ),

    url(
        r'^(?P<category_slug>[\w\-]+)/(?P<slug>[\w\-]+)/send_feedback/$',
        ArticleDetailFeedbackView.as_view(),
        name='article_feedback_form'
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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
