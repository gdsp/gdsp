from django.conf.urls import patterns, include, url

urlpatterns = patterns('tutor.views',
                       url(r'^results/$', 'results'),
                       url(r'^lesson_results/$', 'lesson_results'),
                       url(r'^test_interactive/(?P<test_name>[A-Za-z0-9. ]+)/(?P<level>[A-Za-z0-9 ]+)/(?P<FX>[A-Za-z0-9. ]+)$', 'test_interactive'),
                       url(r'^(?P<test_name>[A-Za-z0-9 ]+)/(?P<level>[A-Za-z0-9 ]+)/(?P<FX>[A-Za-z0-9. ]+)$', 'test')
)
