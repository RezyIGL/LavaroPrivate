from django.urls import path
from . import views

app_name = "LavaroWeb"
urlpatterns = [
    path("Profile/", views.profile),
    path("", views.home),
    path("Chats/", views.chat, name="chats")
]
