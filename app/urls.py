from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from .views import HomeView


admin.site.site_title = 'Knowledge Base'
admin.site.site_header = 'Knowledge Base'


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name='home'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
