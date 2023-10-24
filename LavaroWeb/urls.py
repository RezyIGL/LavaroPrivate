
from django.urls import path, include
from . import views
from .views import SignUpView



app_name = "LavaroWeb"
urlpatterns = [    
    path('signup', SignUpView.as_view(), name='signup'),
    path("Vacancy", views.vacancy_list, name="vacancy_list"),
    path("Profile/<int:user_id>", views.profile_detail, name="profile_detail"), 
    path("Chats", views.chat, name="chats"),
    path("Vacancy/<int:vacancy_id>", views.vacancy_detail, name="vacancy_detail"), 
]

