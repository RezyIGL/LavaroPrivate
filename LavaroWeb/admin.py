from django.contrib import admin

from .models import MyUser, UserProfile, Vacancy

# Register your models here.


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'salary']
    list_filter = ['created', 'publish', 'author', 'salary']
    search_fields = ['title', 'author', 'requirement']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish']
    

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'age', 'expirience', 'image']
    list_filter = ['age', 'expirience']
    search_fields = ['name']
    raw_id_fields = ['user']