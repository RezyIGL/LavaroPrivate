from django.urls import path, include
from . import views
from .views import SignUpView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = "LavaroWeb"

urlpatterns = [
    path('login/', TemplateView.as_view(template_name='registration/login.html'), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path("Vacancy", views.Vacancy_list_View.as_view(), name="vacancy_list"),
    path("Profile/<int:user_id>", views.profile_detail, name="profile_detail"), 
    path("Chats", views.chat, name="chats"),
    
    #new profile for unique user
    path('userProfile', views.user_profile, name="user-profile"),
    
    #new vacancy constructor
    path("VacancyConstructor", views.vacancy_create, name="vacancy_create"),
    
    #new
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    
    path("chats/", views.Chat_list_View.as_view(), name="chats_list"),
    path("chats/<int:chat_id>", views.chat_detail, name="chat_detail"),
    path("chats/<int:chat_id>/add", views.add_participant, name="add_participant"),
    
    path("Vacancy/<int:vacancy_id>", views.Vacancy_detait_View.as_view(), name="vacancy_detail"), 
]

