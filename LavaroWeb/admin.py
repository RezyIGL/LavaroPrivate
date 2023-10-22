from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import MyUser, UserProfile, Vacancy, Chat

# Register your models here.


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'salary']
    list_filter = ['created', 'publish', 'author', 'salary']
    search_fields = ['title', 'author', 'requirement']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish']


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = ['email', 'username',]

admin.site.register(MyUser, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'age', 'expirience', 'image']
    list_filter = ['age', 'expirience']
    search_fields = ['name']
    raw_id_fields = ['user']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "last_modified"]
    list_filter = ["last_modified"]
    search_fields = ["participants"]
    date_hierarchy = "last_modified"
    ordering = ["last_modified"]