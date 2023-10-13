from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
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


def vacancy_list(request):
    template_name = "LavaroWeb/vacancy/list.html" # тут представление главной страницы (расположены все вакансии), нужен "main.html"
    plenty_vacancy = Vacancy.objects.all()

    return render(request, template_name, {'plenty_vacancy': plenty_vacancy})


def profile_detail(request, profile_id):
    template_name = "LavaroWeb/profile/detail.html" # тут подправил (советую изменить свою часть)
    try:
        profile = UserProfile.objects.get(id=profile_detail)
    except UserProfile.DoesNotExist:
        raise Http404("No Profile found.")

    return render(request, template_name, {'profile': profile})


def chat(reguest):
    template_name = "LavaroWeb/chat/detail.html" # нет файла "html" и нужно доделать
    return HttpResponse("Chat")


def vacancy_detail(request, vacancy_id):
    template_name = "LavaroWeb/vacancy/detail.html"  # аналогично менял
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        raise Http404("No Vacancy found.")
    
    return render(request, template_name, {'vacancy': vacancy})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")