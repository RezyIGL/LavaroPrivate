from django.urls import path
from . import views
from .views import SignUpView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.base import RedirectView

app_name = 'LavaroWeb'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('Vacancy/', views.Vacancy_list_View.as_view(), name='vacancy_list'),
    path('Profile/<int:pk>', views.ProfileDetail.as_view(), name='profile_detail'), 
    path('Chats', views.chat, name='chats'),
    path('userProfile', views.User_Profile_View.as_view(), name='user-profile'),
    path('userProfile/change_password', views.Change_Password_Views.as_view(), name='change_password'),
    path('response/<int:vacancy_id>', views.Do_responce_View.as_view(), name='response'),
    path('Vacancy/Constructor', views.Vacancy_create_View.as_view(), name='vacancy_create'),
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password-reset'),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('chats/', views.Chat_list_View.as_view(), name='chats_list'),
    path('chat/<int:pk>', views.MessageListForChat.as_view(), name='chat_detail'),
    #TODO -> добавить кнопку на странице конкретного чата для добавления участника в группу этого чата
    path('chats/<int:chat_id>/add', views.Add_participant_View.as_view(), name='add_participant'),
    path('chats/<int:chat_id>/delete', views.Chat_delete_View.as_view(), name='chat_delete'),
    path('chats/<int:chat_id>/leave', views.Chat_leave_View.as_view(), name='chat_leave'),
    path('Vacancy/<int:pk>/', views.VacancyDetail.as_view(), name='vacancy_detail'),
]
