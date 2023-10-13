from django.db import models
from django.utils import timezone
from django.contrib import admin
from django import forms
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.DateField(null=True, blank=True)
    expirience = models.FloatField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


class Vacancy(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='vacancy')
    requirement = models.TextField(max_length=500)
    title = models.CharField(max_length=100)
    salary = models.FloatField(null=True, blank=True)
    additionalDate = models.TextField(max_length=200, null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
    
    def __str__(self):
        return self.title


class Response(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)


class Chat(models.Model):
    name = models.CharField(max_length=255)


class UserChat(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT)


class Message(models.Model):
    auther = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='message')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
