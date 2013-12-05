from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from views import (LessonsListView, LessonDetailView, TopicsListView,
                   TopicDetailView)

urlpatterns = patterns('',
    url(r'^$', login_required(LessonsListView.as_view()), name='lessons'),
    url(r'^(?P<pk>\d+)(?:/(?P<topic>\d+))?/$', LessonDetailView.as_view(),
        name='lesson'),
    url(r'^topics/$', TopicsListView.as_view(), name='topics'),
    url(r'^topics/(?P<pk>\d+)/$', TopicDetailView.as_view(), name='topic'),
)
