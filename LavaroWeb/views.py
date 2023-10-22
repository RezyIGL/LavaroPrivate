from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, \
                                        Http404
from django.db import models
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required

from .models import MyUser, UserProfile, Vacancy, Response, \
    Chat, UserChat, Message
# Create your views here.

def home(request):
    template_name = "LavaroWeb/home.html"

    return render(request, template_name)


def vacancy_list(request):
    template_name = "LavaroWeb/vacancy/list.html" # тут представление главной страницы (расположены все вакансии), нужен "main.html"
    vacancy_list = Vacancy.objects.all()
    paginator = Paginator(vacancy_list, 8)
    page_number = request.GET.get('page', 1)
    try:
        plenty_vacancy = paginator.page(page_number)
    except PageNotAnInteger:
        plenty_vacancy = paginator.page(1)
    except EmptyPage:
        plenty_vacancy = paginator.page(paginator.num_pages)

    return render(request, template_name, {'plenty_vacancy': plenty_vacancy})

# altenative vacancy list view (class)
'''class VacancyListView(ListView):
    queryset = Vacancy.objects.all()
    context_object_name = 'plenty_vacancy'
    paginate_by = 8
    template_name = "LavaroWeb/vacancy/list.html"
'''
#==============================================================

def profile_detail(request, user_id):
    template_name = "LavaroWeb/profile/detail.html" # тут подправил (советую изменить свою часть)
    try:
        profile = UserProfile.objects.get(id=user_id)
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


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'singup.html'