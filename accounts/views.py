from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView


def home_login(request, template):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    return render(request, template, {"login_form": login_form,
                                      "register_form": register_form})

class RegisterView(TemplateView):
    template_name = 'accounts/home.html'

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
                return HttpResponseRedirect(reverse('home'))
        else:
            form = UserCreationForm()
        return render(request, self.__class__.template_name, {'form': form})
