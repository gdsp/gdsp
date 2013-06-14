from django.views.generic import TemplateView

from models import BaseLessonElement

class IndexView(TemplateView):
    template_name = 'lessons/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['elements'] = BaseLessonElement.objects.select_subclasses()
        return context
