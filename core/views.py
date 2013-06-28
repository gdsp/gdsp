import json

from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic import ListView, DetailView

from models import Topic, BaseTopicElement, LowerCaseTag

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

def tag_autocomplete_view(request):
    """
    Takes a search term, wrapped in the request's POST data, and returns
    a JSON list of tags whose names start with that term.
    """
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    term = request.POST.get('term', None)
    if not term:
        return HttpResponse(status=204)  # 204 No Content
    tags = LowerCaseTag.objects.filter(name__istartswith=term)[:7]
    json_data = json.dumps([tag.name for tag in tags])
    return HttpResponse(json_data, mimetype='application/json')
