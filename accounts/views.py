from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        super(RegisterView, self).dispatch(request, *args, **kwargs)
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                )
                login(request, user)
                return HttpResponseRedirect(reverse('core:lessons'))
        else:
            form = UserCreationForm()
        return render(request, self.__class__.template_name, {'form': form})
