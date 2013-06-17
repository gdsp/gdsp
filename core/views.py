from django.views.generic import ListView, DetailView

from models import Lesson, BaseLessonElement

class LessonsListView(ListView):
    model = Lesson
    template_name = 'lessons/index.html'
    queryset = Lesson.objects.all()
    context_object_name = 'lessons'

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lessons/lesson.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        context['elements'] = BaseLessonElement.objects.select_subclasses()
        return context
