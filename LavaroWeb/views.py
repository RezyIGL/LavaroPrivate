from django.shortcuts import render
from django.http import HttpResponse

from .models import MyUser, UserProfile, Vacancy, Response, \
    Chat, UserChat, Message

# Create your views here.
def home(request):
    template_name = "LavaroWeb/home.html"

    return render(request, template_name)


def profile(request):
    template_name = "LavaroWeb/profile.html"

    return render(request, template_name)


def chat(reguest):
    return HttpResponse('<h1>Chats</h1>')


def vacancy(request, id):
    return HttpResponse('<h2>Vacancy {id}</h2>')