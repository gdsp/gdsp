from django.conf import settings
from django.conf.urls import patterns, include, url, static
from os import environ

from django.contrib import admin
admin.autodiscover()

from pages.views import HomeView, AboutView, PnaclView

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

    # The automatic tutor app:
    url(r'^tutor/', include('tutor.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
#     {'document_root': '/srv/www/gdsp.hf.ntnu.no/data/', 'show_indexes': True}),
     {'document_root': '/Users/tidemann/Documents/NTNU/gdsp/data/', 'show_indexes': True}),

    # Static pages such as the home page, 'About' etc.:
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^pnacl/$', PnaclView.as_view(), name='pnacl'),
)

if not environ.get('DJANGO_PRODUCTION', None):
    urlpatterns += static.static(settings.MEDIA_URL,
                                 document_root=settings.MEDIA_ROOT)
