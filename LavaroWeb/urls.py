from django.urls import path, re_path

from . import views

app_name = "LavaroWeb"
urlpatterns = [    
    path("", views.home, name="welcomePage"),
    path("Vacancy", views.vacancy_list, name="vacancy_list"),
    #path("Vacancy", views.VacancyListView.as_view(), name="vacancy_list"),
    path("Profile/<int:profile_id>", views.profile_detail, name="profile_detail"), # тут добавил "/<int:profile_id>" и поменял "views.profile" на "views.profile_detail"
    path("Chats", views.chat, name="chats"),
    path("Vacancy/<int:vacancy_id>", views.vacancy_detail, name="vacancy_detail"), # тут поменял "views.vacancy" на "views.vacancy_detail"
]


