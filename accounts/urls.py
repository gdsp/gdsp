from django.conf.urls import patterns, include, url
from django.contrib import auth

from views import RegisterView

urlpatterns = patterns('',
        url(r'^login/$',
            'accounts.views.home_login',
            {'template': 'accounts/login.html'},
            name='login'),                       
        url(r'^login_return/$',
            'django.contrib.auth.views.login',
            kwargs={'template_name': 'accounts/login.html'},
            name='login_return',),
        url(r'^logout/$',
            'django.contrib.auth.views.logout',
            kwargs={'next_page': '/'},
            name='logout',),
        url(r'^register/$',
            RegisterView.as_view(),
            name='register'),
)
