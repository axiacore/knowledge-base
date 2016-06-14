from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from .views import HomeView, CategoryDefaultView, ArticleDefaultView


admin.site.site_title = 'Knowledge Base'
admin.site.site_header = 'Knowledge Base'


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name='home'),
    url(
        r'^categoria/(?P<slug>[\w\-]+)/$',
        CategoryDefaultView.as_view(),
        name='CategoryDefaultView'
        ),
    url(
        r'^articulo/(?P<slug>[\w\-]+)/$',
        ArticleDefaultView.as_view(),
        name='ArticleDefaultView'
        ),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
