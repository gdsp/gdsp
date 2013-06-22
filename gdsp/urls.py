from django.conf import settings
from django.conf.urls import patterns, include, url, static
from os import environ

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gdsp.views.home', name='home'),

    url(r'^topics/', include('core.urls', app_name='core', namespace='core')),
    url(r'^admin/', include(admin.site.urls)),
)

if not environ.get('DJANGO_PRODUCTION', None):
    urlpatterns += static.static(settings.MEDIA_URL,
                                 document_root=settings.MEDIA_ROOT)
