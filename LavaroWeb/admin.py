from django.contrib import admin

from .models import MyUser, UserProfile, Vacancy

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(MyUser)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'salary']
    list_filter = ['created', 'publish', 'author', 'salary']
    search_fields = ['title', 'author', 'requirement']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish']
    