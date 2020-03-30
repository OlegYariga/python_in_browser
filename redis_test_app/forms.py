from django.forms import ModelForm
from .models import Student
from django import forms


class RegistrationForm(ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'password', 'first_name', 'last_name', 'status', 'group']

    def saveuser(self):
        user = self.save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
