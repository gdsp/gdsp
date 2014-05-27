from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'pages/home.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class PnaclView(TemplateView):
    template_name = 'pages/home.html'
