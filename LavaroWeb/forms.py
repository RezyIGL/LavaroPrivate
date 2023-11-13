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

class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    age = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control-file'}))
    expirience = forms.FloatField()
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'expirience', 'image']