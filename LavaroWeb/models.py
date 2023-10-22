from django.db import models
from django.utils import timezone
from django.contrib import admin
from django import forms
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.
class MyUser(AbstractUser):
    
    def __str__(self):
        return "{}".format(self.username)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    age = models.DateField(null=True, blank=True)
    expirience = models.FloatField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__ (self):
        return str(self.user)

class Vacancy(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='vacancy')
    requirement = models.TextField()
    title = models.CharField(max_length=500)
    salary = models.FloatField(null=True, blank=True)
    additionalDate = models.TextField( null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("LavaroWeb:vacancy_detail", args=[self.id])
    


class Response(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)


class Chat(models.Model):
    participants = models.ManyToManyField(MyUser, related_name="chats")
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_modified']
        indexes = [models.Index(fields=['-last_modified'])]
    
    
    def __str__(self):
        return f"Chat {self.id}: [{', '.join([p.username for p in self.participants.all()])}]"


class Message(models.Model):
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="sent_message")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="message")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.id}: {self.sender} to {self.chat}"