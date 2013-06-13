from django.views.generic import TemplateView

from models import MarkdownElement

class IndexView(TemplateView):
    template_name = 'lessons/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['elements'] = MarkdownElement.objects.all()
        return context
