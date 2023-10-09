from django.contrib import admin

from .models import MyUser, UserProfile, Vacancy

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Vacancy)
admin.site.register(MyUser)