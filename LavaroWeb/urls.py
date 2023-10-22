from django.urls import path
from . import views
from .views import SignUpView



app_name = "LavaroWeb"
urlpatterns = [    
    path("", views.home, name="welcomePage"),
    path('singup/', SignUpView.as_view(), name='singup'),
    path("Vacancy", views.vacancy_list, name="vacancy_list"),
    path("Profile/<int:profile_id>", views.profile_detail, name="profile_detail"), 
    path("Chats", views.chat, name="chats"),
    path("Vacancy/<int:vacancy_id>", views.vacancy_detail, name="vacancy_detail"), 
]


