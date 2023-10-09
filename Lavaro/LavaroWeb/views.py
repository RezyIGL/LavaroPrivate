from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import MyUser, UserProfile, Vacancy, Response, \
    Chat, UserChat, Message
# Create your views here.

def home(request):
    return HttpResponse('<h1>Main page</h1>')


def profile(request):
    return HttpResponse('<h1>Profile</h1>')


def chat(reguest):
    return HttpResponse('<h1>Chats</h1>')


def vacancy(request, id):
    return HttpResponse('<h2>Vacancy {id}</h2>')


