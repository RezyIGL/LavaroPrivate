from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver 
from .models import UserProfile, MyUser, Vacancy

@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=MyUser)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# @receiver(post_save, sender=MyUser)
# def create_vacancy(sender, instance, created, **kwargs):
#     if created:
#         Vacancy.objects.create(user=instance)


# @receiver(post_save, sender=MyUser)
# def save_vacancy(sender, instance, **kwargs):
#     instance.vacancy.save()

