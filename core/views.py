import json

from django.http import HttpResponse, HttpResponseNotAllowed, Http404
from django.views.generic import ListView, DetailView

from models import (Lesson, Topic, LessonTopicRelation, BaseTopicElement,
                    LowerCaseTag)

class TopicsListView(ListView):
    model = Topic
    template_name = 'core/topics/index.html'
    queryset = Topic.objects.order_by('title')
    context_object_name = 'topics'


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'core/topics/topic.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['elements'] = BaseTopicElement.objects.filter(
                topic_id=self.kwargs['pk'],
        ).select_subclasses()
        return context


class LessonsListView(ListView):
    model = Lesson
    template_name = 'core/lessons/index.html'
    queryset = Lesson.objects.all()
    context_object_name = 'lessons'


class LessonDetailView(DetailView):
    model = Lesson
    context_object_name = 'lesson'
    template_name = 'core/lessons/lesson.html'

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        topic_id = self.kwargs.get('topic', None)
        if topic_id:
            try:
                topic = self.object.topics.get(id=topic_id)
            except Topic.DoesNotExist:
                raise Http404
        else:
            topic = LessonTopicRelation.objects.first(self.object).topic
        context['lesson_topic'] = LessonTopicRelation.objects.get(
                lesson=self.object.id,
                topic=topic.id,
        )
        context['lessons'] = Lesson.objects.all()
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
