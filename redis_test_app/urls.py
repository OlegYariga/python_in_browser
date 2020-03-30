"""redistest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import MyView, LoginView, LogoutView, RegistrationView


urlpatterns = [
    path('setenviroment/', MyView.as_view(_pass_template_name='setenviroment.html')),
    path('baseconstructions/', MyView.as_view(_pass_template_name='baseconstructions.html')),
    path('matplotlib/', MyView.as_view(_pass_template_name='matplotlib.html')),
    path('datacollect/', MyView.as_view(_pass_template_name='datacollect.html')),
    path('datasave/', MyView.as_view(_pass_template_name='datasave.html')),
    path('dataload/', MyView.as_view(_pass_template_name='dataload.html')),
    path('python_and_osc/', MyView.as_view(_pass_template_name='python_and_osc.html')),
    path('comments/', MyView.as_view(_pass_template_name='comments.html')),
    path('smoothing/', MyView.as_view(_pass_template_name='smoothing.html')),
    path('gaussian/', MyView.as_view(_pass_template_name='gaussian.html')),
    path('jdx/', MyView.as_view(_pass_template_name='jdx.html')),
    path('managering_program/', MyView.as_view(_pass_template_name='managering_program.html')),
    path('arduino/', MyView.as_view(_pass_template_name='arduino.html')),
    path('ni/', MyView.as_view(_pass_template_name='ni.html')),
    path('detection/', MyView.as_view(_pass_template_name='detection.html')),
    path('view_and_save_results/', MyView.as_view(_pass_template_name='view_and_save_results.html')),
    path('database/', MyView.as_view(_pass_template_name='database.html')),
    path('final_comments/', MyView.as_view(_pass_template_name='final_comments.html')),
    path('', MyView.as_view(_pass_template_name='setenviroment.html')),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('registration/', RegistrationView.as_view()),
]
