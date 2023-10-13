from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db import models
from django.urls import reverse
from django.views import generic
from django.utils import timezone

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


def vacancy(request, vacancy_id):
    return HttpResponse(f'<h2>Vacancy {vacancy_id}</h2>')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")