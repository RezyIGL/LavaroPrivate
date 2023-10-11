from django.urls import path, re_path

from . import views

app_name = "LavaroWeb"
urlpatterns = [    
    path("", views.home, name="welcomePage"),
    path("Profile", views.profile, name="profilePage"),
    path("Chats", views.chat, name="chats"),
    path("Vacancy/<int:vacancy_id>", views.vacancy)
]


