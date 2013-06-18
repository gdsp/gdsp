from django.views.generic import ListView, DetailView

from models import Topic, BaseTopicElement

class TopicsListView(ListView):
    model = Topic
    template_name = 'topics/index.html'
    queryset = Topic.objects.all()
    context_object_name = 'topics'

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topics/topic.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['elements'] = BaseTopicElement.objects.filter(
                topic_id=self.kwargs['pk']).select_subclasses()
        return context
