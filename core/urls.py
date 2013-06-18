from django.conf.urls import patterns, include, url

from views import TopicsListView, TopicDetailView

urlpatterns = patterns('',
    url(r'^$', TopicsListView.as_view(), name='topics'),
    url(r'^(?P<pk>\d+)', TopicDetailView.as_view(), name='topic'),
)
