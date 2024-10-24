from typing import Any
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Talk
from django import forms
from allauth.account.forms import SignupForm


class UserModelForm(UserCreationForm):

    class Meta:
        model = User # 使用するmodelを指定
    # 表示するフォームを指定
        fields = ('username', 'email', 'password1',"password2","img")

        labels = {
          "username": "Username",
          "email": "Email address",
          "password1": "Password",
          "password2":"Password confirmation",
          "img":"Image"
        }

class UserLoginForm(AuthenticationForm):
    fields = ('username', 'password')

    labels = {
        "username":"Username",
        "password":"Password"
    }

class MySignupForm(SignupForm):
    image = forms.ImageField()
    
    def signup(self, request, user):
        user.img = self.cleaned_data['image']
        user.save()
        return user
    
