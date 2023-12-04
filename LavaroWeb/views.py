from typing import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import CustomUserCreationForm, ProfileUpdateForm, CreateVacancy, PasswordUpdate, ChangeVacancyForm
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from . import serializers
from .models import MyUser, UserProfile, Vacancy, Chat, Message
import json


class Home_View(ListView):
    template_name = "registration/login.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class ProfileList(APIView):
    queryset = Vacancy.objects.all()
    serializer_class = serializers.UserProfileSerializer
    
    @swagger_auto_schema(responses={200: serializers.UserProfileSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        serializer = serializers.UserProfileSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProfileDetail(APIView):
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    @swagger_auto_schema(responses={200: serializers.UserProfileSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return Response({'things': self.queryset}, template_name="profile/detail.html")
        
        profile = get_object_or_404(self.queryset, id=kwargs['pk'])
        serializer = serializers.UserProfileSerializer(profile)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='PUT /profile/{id}/', 
                        request_body=serializers.PartitialUpdateUserProfileSerializer(),
                        responses={200: serializers.UserProfileSerializer()})
    def put(self, request, *args, **kwargs):
        profile = get_object_or_404(self.queryset, id=kwargs['pk'])
        serializer = serializers.UserProfileSerializer(profile, data=request.data | {"user": kwargs['pk']})
        if serializer.is_valid():
            # serializer.update(profile, request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description='', 
                        request_body=serializers.PartitialUpdateUserProfileSerializer(),
                        responses={200: serializers.UserProfileSerializer()})
    def patch (self, request, *args, **kwargs):
        profile = get_object_or_404(self.queryset, id=kwargs['pk'])
        serializer = serializers.PartitialUpdateUserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            # serializer.update(profile, request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class User_Profile_View(ListView):
#     template_name = "profile/user_profile.html"
#     context_object_name = "profile_form"
    
#     def post(self, request, *args, **kwargs):
#         profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
#         if profile_form.is_valid():
#             profile = request.user.userprofile
#             profile.name = request.POST['name']
#             profile.age = request.POST['age']
#             profile.expirience = request.POST['expirience']
#             profile.image = profile.image
#             profile.save()
#             profile_form.save()
        
#         else:
#             return profile_form.errors
        
#         return render(request, template_name=self.template_name, context={self.context_object_name: profile_form})
    
#     def get(self, request, *args, **kwargs):
#         profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        
#         return render(request, template_name=self.template_name, context={self.context_object_name:profile_form})


class Change_Password_Views(ListView):
    template_name = 'profile/change_password.html'
    context_object_name = 'password_form'
    
    def post(self, request, *args, **kwargs):
        
        if request.POST['password1'] == request.POST['password2']:
            user = request.user
            user.set_password(request.POST['password1'])
            user.save()
        
        return redirect(to="/")
    
    def get(self, request, *args, **kwargs):
        password_form = PasswordUpdate()
        
        return render(request, self.template_name, context={self.context_object_name: password_form})


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


class VacancyList(APIView):
    queryset = Vacancy.objects.all()
    serializer_class = serializers.VacancySerializer
    
    def get(self, request, *args, **kwargs):
        serializer = serializers.VacancySerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.VacancySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VacancyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = serializers.VacancySerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    @swagger_auto_schema(responses={200: serializers.VacancySerializer()})
    def get(self, request, *args, **kwargs):

        if request.accepted_renderer.format == 'html':
            return Response({'things': self.queryset}, template_name="vacancy/detail.html")

        pk = kwargs["pk"]
        vacancy = get_object_or_404(self.queryset, id=pk)
        serializer = serializers.VacancySerializer(vacancy)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_description='PUT /vacancy/{id}/',
                         request_body=serializers.PartialUpdateVacancySerializer(),
                         responses={200: serializers.VacancySerializer()})
    def put (self, request, *args, **kwargs):
        if Vacancy.objects.get(id=kwargs['pk']).author == request.user:
            return self.update(request, *args, **kwargs)
        return Http404("NEL'Z'A")
        
    @swagger_auto_schema(operation_description='',
                        request_body=serializers.PartialUpdateVacancySerializer(),
                        responses={200: serializers.VacancySerializer()})
    def patch(self, request, *args, **kwargs):
        if Vacancy.objects.get(id=kwargs['pk']).author == request.user:
            return self.update(request, *args, **kwargs | {"partial": True})
        return Http404("NEL'Z'A")
    
    @swagger_auto_schema(operation_description='DELETE /vacancy/{id}')
    def delete (self, request, *args, **kwargs):
        pk = kwargs["pk"]
        vacancy = get_object_or_404(self.queryset, id=pk)
        if vacancy.author == request.user:
            vacancy.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Http404("NEL'Z'A")


class Vacancy_create_View(ListView):
    template_name = "vacancy/create_form.html"
    context_object_name = "vacancy_form"
    
    def post(self, request, *args, **kwargs):
        vacancy_form = CreateVacancy(request.POST)
        
        if vacancy_form.is_valid():
            
            vacancy = Vacancy.objects.create(author=request.user)
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


# class Vacancy_reduction_View(ListView):
#     template_name = 'vacancy/reduction.html'
#     context_object_name = 'vacancy_form'
    
#     def post(self, request, *args, **kwargs):
#         vacancy_form = ChangeVacancyForm(request.POST)
        
#         if vacancy_form.is_valid():
            
#             vacancy = Vacancy.objects.get(author=request.user)
#             vacancy.title=request.POST['title']
#             vacancy.requirement=request.POST['requirement']
#             vacancy.salary=request.POST['salary']
#             vacancy.additionalDate = request.POST['additionalDate']
#             vacancy.save()
#             return HttpResponseRedirect(reverse("LavaroWeb:vacancy_detail", args=[vacancy.id]))
#         else:
#             return vacancy_form.errors
    
#     def get(self, request, *args, **kwargs):
#         vacancy_form = ChangeVacancyForm()
        
#         return render(request, template_name=self.template_name, context={self.context_object_name: vacancy_form})


# class Vacancy_delete_View(ListView):
    
#     def get (self, request, vacancy_id, *args, **kwargs):
#         vacancy = Vacancy.objects.get(id = vacancy_id)
#         vacancy.delete()
#         return HttpResponseRedirect(reverse("LavaroWeb:vacancy_list"))
    

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


def chat(request):
    template_name = "chat/detail.html"
    return HttpResponse(request, template_name)


class Chat_list_View(ListView):
    template_name = "chat/chats_list.html"
    context_object_name = "chats"
    
    def get (self, request, *args, **kwargs):
        chats = request.user.chats.order_by("-last_modified")
        return render(request, template_name=self.template_name, context={self.context_object_name: chats})
    
    def post (self, request, *args, **kwargs):
        chats = request.user.chats.order_by("-last_modified")
        return render(request, template_name=self.template_name, context={self.context_object_name: chats})


class MessageListForChat(APIView):
    queryset = Message.objects.all()
    serializer_class = serializers.Messageserializer

    @swagger_auto_schema(responses={200: serializers.Messageserializer(many=True)})
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        messages = self.queryset.filter(chat=pk)
        serializer = serializers.Messageserializer(messages, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description='POST /chat/{id}')
    def post(self, request, *args, **kwargs):
        serializer = serializers.Messageserializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")