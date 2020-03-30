from uuid import uuid4
from django.shortcuts import render
from django.views.generic import View
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login


from .forms import RegistrationForm, LoginForm
from .models import Student

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class MyView(View):
    """
        Base view for the part one
    """
    _pass_template_name = None

    def __init__(self, **kwargs):
        self._templates_name_list = ['setenviroment.html',
                                     'baseconstructions.html',
                                     'matplotlib.html',
                                     'datacollect.html']
        self._pass_template_name = kwargs['_pass_template_name']
        super().__init__()

    def get(self, request):
        if self._pass_template_name in self._templates_name_list:
            return render(request, template_name=self._pass_template_name)
        return redirect('/')


class LoginView(View):
    """
    Provides the ability to login as a user with a username and password
    """
    def __init__(self):
        self._template_name = 'header.html'
        super().__init__()

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, template_name=self._template_name, context={'begin_auth': True, 'form': form,
                                                                                       'msg':'User is disabled by admin'})
            else:
                return render(request, template_name=self._template_name, context={'begin_auth': True, 'form': form,
                                                                                   'msg':'Invalid email or password'})


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    def __init__(self):
        self._url = '/login/'

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        auth_logout(request)
        return redirect("/")


class RegistrationView(View):
    """
        Provides users the ability to register in system
    """
    def __init__(self):
        self._form = RegistrationForm()
        self._template_name = 'registration.html'
        super().__init__()

    def get(self, request):
        return render(request, template_name=self._template_name, context={'form': self._form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.saveuser()
            return render(request, template_name=self._template_name, context={'begin_auth': True, 'form': None})
        return render(request, template_name=self._template_name, context={'form': form})
