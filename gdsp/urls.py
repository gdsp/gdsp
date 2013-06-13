from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gdsp.views.home', name='home'),

    url(r'^lessons/', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
