from django.conf.urls import patterns, include, url
from django.contrib import auth

urlpatterns = patterns('',
        url(r'^login/$', 'django.contrib.auth.views.login',
            kwargs={'template_name': 'accounts/login.html'},
            name='login',
        ),
        url(r'^logout/$', 'django.contrib.auth.views.logout',
            kwargs={'next_page': '/lessons/'},
            name='logout',
        ),
)
