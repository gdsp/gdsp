from django.conf import settings
from django.conf.urls import patterns, include, url, static
from os import environ

from django.contrib import admin
admin.autodiscover()

from pages.views import HomeView, AboutView

urlpatterns = patterns('',
    # Account handling (login, logout, registration, ...):
    url(r'^accounts/', include('accounts.urls', app_name='accounts',
                               namespace='accounts')),

    # Lessons, topics etc.; the meat of the application:
    url(r'^lessons/', include('core.urls', app_name='core', namespace='core')),

    # Autocompletion of tags (for editing of topics):
    url(r'^admin/tag_autocomplete/$', 'core.views.tag_autocomplete_view'),

    # The Django admin app:
    url(r'^admin/', include(admin.site.urls)),

    # Static pages such as the home page, 'About' etc.:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
)

if not environ.get('DJANGO_PRODUCTION', None):
    urlpatterns += static.static(settings.MEDIA_URL,
                                 document_root=settings.MEDIA_ROOT)
