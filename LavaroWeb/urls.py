from django.urls import path, include
from . import views
from .views import SignUpView
from django.views.generic.base import TemplateView

app_name = "LavaroWeb"

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signup', SignUpView.as_view(), name='signup'),
    path("Vacancy", views.vacancy_list, name="vacancy_list"),
    path("Profile/<int:user_id>", views.profile_detail, name="profile_detail"), 
    path("Chats", views.chat, name="chats"),
    path("Vacancy/<int:vacancy_id>", views.vacancy_detail, name="vacancy_detail"), 
]

