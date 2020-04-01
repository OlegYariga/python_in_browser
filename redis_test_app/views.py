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
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


from .forms import RegistrationForm, LoginForm, TestForm, QuestionForm, AnswerForm
from .models import Student, Answer, Question, Test

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
                                     'datacollect.html',
                                     'datasave.html',
                                     'dataload.html',
                                     'python_and_osc.html'


                                     ]
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

    def get(self, request):
        return render(request, template_name=self._template_name, context={'begin_auth': True,
                                                                           'msg': 'Чтобы пройти тест, вы должны '
                                                                                  'авторизоваться или зарегистрироваться'})

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


class TestView(View):

    def __init__(self):
        self._test_form = TestForm()
        self._question_form = QuestionForm()
        self._answer_form = AnswerForm()
        super().__init__()

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        test_id = request.GET.get('test_id', 0)
        test_numbers = Test.objects.filter(id=test_id).first()
        if not test_numbers:
            return redirect('/')
        questions, answers = self._answer_form.select_related_questions(test_id)
        return render(request, template_name='tests/testview.html',
                      context={'test_form': self._test_form,
                               'question_form': self._question_form,
                               'answer_form': self._answer_form,
                               'questions': questions,
                               'answers': answers
                               })

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        test_id = request.GET.get('test_id', 0)
        questions, answers = self._answer_form.select_related_questions(test_id)
        print(request.user.username)
        result, right_questions = self._answer_form.check_answers(test_id, request.POST, request.user.username)

        return render(request, template_name='tests/testview.html',
                      context={'test_form': self._test_form,
                               'question_form': self._question_form,
                               'answer_form': self._answer_form,
                               'questions': questions,
                               'answers': answers,
                               'result': result,
                               'right_questions': right_questions
                               })


class TestCreateView(View):

    def __init__(self):
        self._test_form = TestForm()
        self._question_form = QuestionForm()
        self._answer_form = AnswerForm()
        super().__init__()

    @method_decorator(staff_member_required)
    def get(self, request):
        return render(request, template_name='custom_admin/test_create.html',
                      context={'test_form': self._test_form,
                               'question_form': self._question_form,
                               'answer_form': self._answer_form,
                               'question_nums': [1,2,3,4,5,6,7,8,9,10],
                               })

    @method_decorator(staff_member_required)
    def post(self, request):
        test = TestForm(request.POST)
        print(test)
        test_obj = test.save()
        questions = QuestionForm().set_new_questions_by_test(test_obj, request.POST)
        return redirect('/')

class UserinfoView(View):
    pass