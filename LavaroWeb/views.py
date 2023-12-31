
from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.template.response import SimpleTemplateResponse as STR
from .forms import CustomUserCreationForm, ProfileUpdateForm, CreateVacancy, PasswordUpdate
from django.contrib.auth.decorators import login_required
from django.contrib import messages as mess
from rest_framework.generics import ListAPIView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from .models import MyUser, UserProfile, Vacancy, Response, Chat, Message


#home page
# def home(request):
#     template_name = "registration/login.html"

#     return render(request, template_name)
class Home_View(ListView):
    template_name = "registration/login.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


#profile & response
# def profile_detail(request, user_id):
#     template_name = "profile/detail.html"
#     try:
#         profile = UserProfile.objects.get(id=user_id)
#     except UserProfile.DoesNotExist:
#         raise Http404("No Profile found.")

#     return render(request, template_name, {'profile': profile})
class Profile_detail_View(ListView):
    template_name = "profile/detail.html"
    context_object_name = "profile"
    
    def get(self, request, user_id, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            raise Http404("No Profile found.")

        return render(request, template_name=self.template_name, context={self.context_object_name: profile})


#требует страницы и отладки
# @login_required
# def user_profile(request):
#     template_name = "profile/user_profile.html"
    
#     if request.method == 'POST':
        
#         profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

#         if profile_form.is_valid():
#             print("hello")
#             profile_form.save()
#             mess.success(request, "Your profile is updated successfully")
#             #return ('LavaroWeb:profile_detail' request.user.id)
#         else:
#             return profile_form.errors

#     else:
#         profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    
#     return render(request, template_name, {'profile_form': profile_form})
class User_Profile_View(ListView):
    template_name = "profile/user_profile.html"
    context_object_name = "profile_form"
    
    def post(self, request, *args, **kwargs):
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if profile_form.is_valid():
            profile = request.user.userprofile
            profile.name = request.POST['name']
            profile.age = request.POST['age']
            profile.expirience = request.POST['expirience']
            profile.image = profile.image
            profile.save()
            profile_form.save()
        
        else:
            return profile_form.errors
        
        return render(request, template_name=self.template_name, context={self.context_object_name: profile_form})
    
    def get(self, request, *args, **kwargs):
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        
        return render(request, template_name=self.template_name, context={self.context_object_name:profile_form})


#Нужно доделать
class Change_Password_Views(ListView):
    template_name = 'profile/change_password.html'
    context_object_name = 'password_form'
    
    def post(self, request, *args, **kwargs):
        
        if request.POST['password1'] == request.POST['password2']:
            user = request.user
            user.set_password(request.POST['password1'])
            user.save()
            #password_form.save()
        
        return redirect(to="/")
    
    def get(self, request, *args, **kwargs):
        password_form = PasswordUpdate()
        
        return render(request, self.template_name, context={self.context_object_name: password_form})


# #требует тестирования и отладки
# def do_response(request,vacancy_id):
#     vacancy = Vacancy.objects.get(id=vacancy_id)
#     chats = Chat.objects.filter(participants__in = [vacancy.author]) & Chat.objects.filter(participants__in = [request.user])
#     if chats:
#         print('chat hello', chats, Chat.objects.filter(participants__in = [vacancy.author]))
#         chats = request.user.chats.order_by("-last_modified")
#         return HttpResponseRedirect(reverse("LavaroWeb:chats_list"))
#     chat = Chat.objects.create()
#     chat.participants.add(vacancy.author)
#     chat.participants.add(request.user)
#     chat.save()
#     return  HttpResponseRedirect(reverse("LavaroWeb:chats_list"))
class Do_responce_View(ListView):
    
    def get(self, request, vacancy_id, *args, **kwargs):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        chats = Chat.objects.filter(participants__in = [vacancy.author]) & Chat.objects.filter(participants__in = [request.user])
        if chats:
            print('chat hello', chats, Chat.objects.filter(participants__in = [vacancy.author]))
            chats = request.user.chats.order_by("-last_modified")
            return HttpResponseRedirect(reverse("LavaroWeb:chats_list"))
        chat = Chat.objects.create(vacancy=Vacancy.objects.get(id=vacancy_id))
        chat.participants.add(vacancy.author)
        chat.participants.add(request.user)
        chat.save()
        return  HttpResponseRedirect(reverse("LavaroWeb:chats_list"))


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

        return render (request, template_name=self.template_name, context={self.context_object_name: plenty_vacancy})


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


# @login_required
# def vacancy_create(request):
#     template_name = "vacancy/create_form.html"
#     if request.method == "POST":
#         vacancy_form = CreateVacancy(request.POST, instance=request.user.vacancy)
        
#         if vacancy_form.is_valid():
#             vacancy_form.save()
#             return redirect(to=template_name)
    
#     else:
#         vacancy_form = CreateVacancy(instance=request.user.vacancy)
    
#     return render(request, template_name, {'vacancy_form': vacancy_form})
class Vacancy_create_View(ListView):
    template_name = "vacancy/create_form.html"
    context_object_name = "vacancy_form"
    
    def post(self, request, *args, **kwargs):
        vacancy_form = CreateVacancy(request.POST)
        
        if vacancy_form.is_valid():
            
            vacancy = Vacancy.objects.create(author=request.user)
            #vacancy.author=request.user.id
            vacancy.title=request.POST['title']
            vacancy.requirement=request.POST['requirement']
            vacancy.salary=request.POST['salary']
            vacancy.additionalDate = request.POST['additionalDate']
            vacancy.save()
            return HttpResponseRedirect(reverse("LavaroWeb:vacancy_list"))
        else:
            return vacancy_form.errors

    def get(self, request, *args, **kwargs):
        vacancy_form = CreateVacancy()
        
        return render(request, template_name=self.template_name, context={self.context_object_name: vacancy_form})


class Vacancy_delete_View(ListView):
    
    def get (self, request, vacancy_id, *args, **kwargs):
        vacancy = Vacancy.objects.get(id = vacancy_id)
        vacancy.delete()
        return HttpResponseRedirect(reverse("LavaroWeb:vacancy_list"))
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
# # @login_required
class Chat_list_View(ListView):
    template_name = "chat/chats_list.html"
    context_object_name = "chats"
    
    def get (self, request, *args, **kwargs):
        chats = request.user.chats.order_by("-last_modified")
        return render(request, template_name=self.template_name, context={self.context_object_name: chats})
    
    def post (self, request, *args, **kwargs):
        chats = request.user.chats.order_by("-last_modified")
        return render(request, template_name=self.template_name, context={self.context_object_name: chats})


# @login_required
# def chat_detail(request, chat_id):
#     template_name = "chat/chat_detail.html"
#     chat = get_object_or_404(Chat, id=chat_id)
#     messages = chat.message.all().order_by("timestamp")
#     if request.method == "POST":
#         text = request.POST.get("text")
#         message = Message.objects.create(sender=request.user, chat=chat, text=text)
#         return HttpResponseRedirect(reverse("LavaroWeb:chat_detail", args=[chat_id]))
#     return render(request, template_name, {"chat": chat, "messages": messages})
class Chat_detail_View(ListView):
    template_name = "chat/chat_detail.html"
    context_object_name = ("chat", "messages")

    def post(self, request, chat_id, *args, **kwargs):
        chat = get_object_or_404(Chat, id=chat_id)
        text = request.POST.get("text")
        messages = chat.message.all().order_by("timestamp")

        message = Message.objects.create(sender=request.user, chat=chat, text=text)
        return HttpResponseRedirect(reverse("LavaroWeb:chat_detail", args=[chat_id]))

    def get(self, request, chat_id, *args, **kwargs):
        chat = get_object_or_404(Chat, id=chat_id)
        messages = chat.message.all().order_by("timestamp")
        return render(request, template_name=self.template_name, context={self.context_object_name[0]: chat, self.context_object_name[1]: messages})



# @login_required
# def add_participant(request, chat_id):
#     chat = get_object_or_404(Chat, chat_id)
#     template_name = "chat/add_participant.html"
#     if request.method == "POST":
#         username = request.POST.get("username")
#         user = MyUser.objects.filter(username=username).first()
#         if user:
#             chat.participants.add(user)
#             return HttpResponseRedirect(reverse("LavaroWeb:chat_detail", arg=[chat.id]))
#         return render(request, template_name, {"chat": chat})
class Add_participant_View(ListView):
    template_name = "chat/add_participant.html"
    context_object_name = "chat"
    
    def post(self, request, chat_id, *args, **kwargs):
        chat = get_object_or_404(Chat,id= chat_id)
        username = request.POST.get('username')
        try:
            user = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            raise Http404("No Profile found.")
        if not(user in chat.participants.all()):
            print("hello")
            chat.participants.add(user)
            return HttpResponseRedirect("LavaroWeb:chat_detail", arg=[chat.id])
        return render(request, template_name=self.template_name, context={self.context_object_name: chat})
    
    def get(self, request, chat_id, *args, **kwargs):
        chat = get_object_or_404(Chat, id=chat_id)
        return render(request, template_name=self.template_name, context={self.context_object_name: chat})


class Chat_leave_View(ListView):
    
    def get(self, request, chat_id, *args, **kwargs):
        chat = Chat.objects.get(id = chat_id)
        
        chat.participants.remove(request.user)
        chat.save()
        
        return HttpResponseRedirect(reverse("LavaroWeb:chats_list")) 


class Chat_delete_View(ListView):
    
    def get(self, request, chat_id, *args, **kwargs):
        chat = Chat.objects.get(id = chat_id)
        chat.delete()
        
        return HttpResponseRedirect(reverse("LavaroWeb:chats_list")) 

#page not found
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")