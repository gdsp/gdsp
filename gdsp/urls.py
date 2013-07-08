from django.conf import settings
from django.conf.urls import patterns, include, url, static
from os import environ

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.urls', app_name='accounts',
                               namespace='accounts')),
    url(r'^lessons/', include('core.urls', app_name='core', namespace='core')),
    url(r'^admin/tag_autocomplete/$', 'core.views.tag_autocomplete_view'),
    url(r'^admin/', include(admin.site.urls)),
)

if not environ.get('DJANGO_PRODUCTION', None):
    urlpatterns += static.static(settings.MEDIA_URL,
                                 document_root=settings.MEDIA_ROOT)
