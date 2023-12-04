from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import MyUser, UserProfile, Vacancy

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

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'expirience']


class ChangeVacancyForm(forms.ModelForm):
    
    class Meta:
        model = Vacancy
        fields = ['title', 'requirement', 'salary', 'additionalDate']

class CreateVacancy(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ['title', 'requirement', 'salary', 'additionalDate']


class PasswordUpdate(forms.Form):
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    