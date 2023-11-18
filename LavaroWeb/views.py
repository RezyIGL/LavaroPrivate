
from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.template.response import SimpleTemplateResponse as STR
from .forms import CustomUserCreationForm, ProfileUpdateForm, CreateVacancy
from django.contrib.auth.decorators import login_required
from django.contrib import messages as mess
from rest_framework.generics import ListAPIView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from .models import MyUser, UserProfile, Vacancy, Response, Chat, Message


#home page
def home(request):
    template_name = "registration/login.html"

    return render(request, template_name)

#profile & response
def profile_detail(request, user_id):
    template_name = "profile/detail.html"
    try:
        profile = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        raise Http404("No Profile found.")

    return render(request, template_name, {'profile': profile})

#требует страницы и отладки
@login_required
def user_profile(request):
    template_name = "profile/user_profile.html"
    
    if request.method == 'POST':
        
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if profile_form.is_valid():
            print("hello")
            profile_form.save()
            mess.success(request, "Your profile is updated successfully")
            #return ('LavaroWeb:profile_detail' request.user.id)
        else:
            return profile_form.errors

    else:
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    return render(request, template_name, {'profile_form': profile_form})


# class ChangePasswordViews(SuccessMessageMixin, PasswordChangeView):
#     template_name = 'LavaroWeb/profile/change_password.html'
#     success_message = "Successfully Changed Your Password"
#     success_url = reverse_lazy('user-profile')

#требует тестирования и отладки
def do_response(request,vacancy_id):
    template_name = "chat/chats_list.html"
    chats = Chat.objects.filter(participants__in = [request.user]) & Chat.objects.filter(participants__in=[vacancy_id.author])
    if chats is not None:
        chats = request.user.chats.order_by("-last_modified")
        return render(request, template_name, {"chats": chats})
    chat = Chat.objects.create(participants = [request.user, vacancy_id.author])
    chat.save()
    chats = request.user.chats.order_by("-last_modified")
    return render(request, template_name, {"chats": chats})

#Vacancy

class Vacancy_list_View(ListView):
    
    queryset = Vacancy.objects.all()
    template_name = 'vacancy/list.html'
    context_object_name = 'plenty_vacancy'
    
    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.queryset, 9)
        page_number = request.GET.get('page', 1)
        try:
            plenty_vacancy = paginator.page(page_number)
        except PageNotAnInteger:
            plenty_vacancy = paginator.page(1)
        except EmptyPage:
            plenty_vacancy = paginator.page(paginator.num_pages)

        return STR(template=self.template_name, context={self.context_object_name: plenty_vacancy})


# def vacancy_detail(request, vacancy_id):
#     template_name = "vacancy/detail.html"
#     try:
#         vacancy = Vacancy.objects.get(id=vacancy_id)
#     except Vacancy.DoesNotExist:
#         raise Http404("No Vacancy found.")
    
#     return render(request, template_name, {'vacancy': vacancy})
class Vacancy_detait_View(ListView):
    template_name = "vacancy/detail.html"
    context_object_name = "vacancy"
    
    def get(self, request, vacancy_id, *args, **kwargs):
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise Http404("No Vacancy found.")
        return render(request, self.template_name, context={self.context_object_name: vacancy})


@login_required
def vacancy_create(request):
    template_name = "vacancy/create_form.html"
    if request.method == "POST":
        vacancy_form = CreateVacancy(request.POST, instance=request.user.vacancy)
        
        if vacancy_form.is_valid():
            vacancy_form.save()
            mess.success(request, "Your vacansy is created successfully")
            return redirect(to=template_name)
    
    else:
        vacancy_form = CreateVacancy(instance=request.user.vacancy)
    
    return render(request, template_name, {'vacancy_form': vacancy_form})
#login & signup
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def post(self, request):
        super(CreateView, self).post(request)
        
        username = request.POST['username']
        user_id = MyUser.objects.get(username=username)
        #photo = 
        profile = UserProfile.objects.create(user=user_id)
        profile.save()

        return redirect('index')

#block Chats and Message
def chat(request):
    template_name = "chat/detail.html"
    return HttpResponse(request, template_name)


# @login_required
# def chats_list(request):
#     template_name = "chat/chats_list.html"
#     chats = request.user.chats.order_by("-last_modified")
#     return render(request, template_name, {"chats": chats})
# @login_required
class Chat_list_View(ListView):
    template_name = "chat/chats_list.html"
    context_object_name = "chats"
    
    def get (self, request, *args, **kwargs):
        chats = request.user.chats.order_by("-last_modified")
        return render(request, template_name=self.template_name, context={self.context_object_name: chats})


@login_required
def chat_detail(request, chat_id):
    template_name = "chat/chat_detail.html"
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.message.all().order_by("timestamp")
    if request.method == "POST":
        text = request.POST.get("text")
        message = Message.objects.create(sender=request.user, chat=chat, text=text)
        return HttpResponseRedirect(reverse("LavaroWeb:chat_detail", args=[chat_id]))
    return render(request, template_name, {"chat": chat, "messages": messages})


@login_required
def add_participant(request, chat_id):
    chat = get_object_or_404(Chat, chat_id)
    template_name = "chat/add_participant.html"
    if request.method == "POST":
        username = request.POST.get("username")
        user = MyUser.objects.filter(username=username).first()
        if user:
            chat.participants.add(user)
            return HttpResponseRedirect(reverse("LavaroWeb:chat_detail", arg=[chat.id]))
        return render(request, template_name, {"chat": chat})


#page not found
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")