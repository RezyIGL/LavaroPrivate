from rest_framework import serializers
from .models import MyUser, UserProfile, Vacancy, Message
from django.utils import timezone

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('__all__')
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.expirience = validated_data.get('expirience', instance.expirience)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    
    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)


class VacancySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vacancy
        fields = ('__all__')
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.title = validated_data.get('title', instance.title)
        instance.title = validated_data.get('title', instance.title)
        instance.title = validated_data.get('title', instance.title)
        instance.title = timezone.now()
        instance.save()
        return instance
    
    def create(self, validated_data):
        return Vacancy.objects.create(**validated_data)


class Messageserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ('__all__')
        
    def create(self, validated_data):
        return Message.objects.create(**validated_data)