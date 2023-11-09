from django.urls import path, include
from . import views
from .views import SignUpView
from django.views.generic.base import TemplateView, RedirectView

app_name = "LavaroWeb"

urlpatterns = [
    path('', RedirectView.as_view(url="login"), name='index'),
    path('login/', TemplateView.as_view(template_name='registration/login.html'), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path("Vacancy", views.vacancy_list, name="vacancy_list"),
    path("Profile/<int:user_id>", views.profile_detail, name="profile_detail"), 
    path("Chats", views.chat, name="chats"),
    
    #new
    path("chats/", views.chats_list, name="chats_list"),
    path("chats/<int:chat_id>", views.chat_detail, name="chat_detail"),
    path("chats/<int:chat_id>/add", views.add_participant, name="add_participant"),
    
    path("Vacancy/<int:vacancy_id>", views.vacancy_detail, name="vacancy_detail"), 
]

