from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser, UserProfile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ('username', 'email')

