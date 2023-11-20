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
    path("Profile/<int:user_id>", views.Profile_detail_View.as_view(), name="profile_detail"), 
    path("Chats", views.chat, name="chats"),
    
    #new profile for unique user
    path('userProfile', views.User_Profile_View.as_view(), name="user-profile"),
    #нужна какая-то заглушка
    path('response/<int:vacancy_id>', views.Do_responce_View.as_view(), name='response'),
    
    #new vacancy constructor
    path("VacancyConstructor", views.Vacancy_create_View.as_view(), name="vacancy_create"),
    
    #new
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    
    path("chats/", views.Chat_list_View.as_view(), name="chats_list"),
    path("chats/<int:chat_id>", views.Chat_detail_View.as_view(), name="chat_detail"),
    #добавить кнопку на странице конкретного чата для добавления участника в группу этого чата
    path("chats/<int:chat_id>/add", views.Add_participant_View.as_view(), name="add_participant"),
    
    path("Vacancy/<int:vacancy_id>", views.Vacancy_detait_View.as_view(), name="vacancy_detail"), 
]

