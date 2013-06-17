from django.conf.urls import patterns, include, url

from views import LessonsListView, LessonDetailView

urlpatterns = patterns('',
    url(r'^$', LessonsListView.as_view(), name='lessons'),
    url(r'^(?P<pk>\d+)', LessonDetailView.as_view(), name='lesson'),
)
