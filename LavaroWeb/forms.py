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
    # name = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    # age = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control-file'}))
    # expirience = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control-file'}))
    # image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'expirience']


class CreateVacancy(forms.ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # requirement = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    # salary = forms.IntegerField()
    # additionalDate = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancy
        fields = ['title', 'requirement', 'salary', 'additionalDate']


class PasswordUpdate(forms.Form):
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    