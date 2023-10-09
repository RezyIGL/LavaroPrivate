from django.db import models
from django.utils import timezone
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class MyUser(models.Model):
    login = models.EmailField()
    password = models.CharField(max_length=100)



class UserProfile(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.DateTimeField(null=True, blank=True)
    expirience = models.FloatField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


class Vacancy(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    requirement = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    salary = models.FloatField(null=True, blank=True)
    additionalDate = models.CharField(max_length=200, null=True, blank=True)


class Response(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)


class Chat(models.Model):
    name = models.CharField(max_length=255)


class UserChat(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT)


class Message(models.Model):
    auther = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
