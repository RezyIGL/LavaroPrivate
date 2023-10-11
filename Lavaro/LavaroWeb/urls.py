from django.urls import path, re_path

from . import views

app_name = "LavaroWeb"
urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    
    path("Profile", views.profile, name="profilePage"),
    path("", views.home, name="welcomePage"),
    path("Chats", views.chat, name="chats"),
    path("Vacancy/<int:vacancy_id>", views.vacancy)
]


