from rest_framework import serializers
from .models import MyUser, UserProfile, Vacancy, Message
from django.utils import timezone

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("__all__")
        


class PartitialUpdateUserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    age = serializers.DateField(required=False)
    expirience = serializers.FloatField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'expirience', 'image']

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.age = validated_data.get('age', instance.age)
            instance.expirience = validated_data.get('expirience', instance.expirience)
            instance.image = validated_data.get('image', instance.image)
            instance.save()
            return instance


class VacancySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vacancy
        fields = ('__all__')


class PartialUpdateVacancySerializer(serializers.ModelSerializer):
    requirement = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    salary = serializers.FloatField(required=False)
    additionalDate = serializers.CharField(required=False)
    
    class Meta:
        model = Vacancy
        fields = ["requirement", "title", "salary", "additionalDate"]

    def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.age = validated_data.get('age', instance.age)
            instance.expirience = validated_data.get('expirience', instance.expirience)
            instance.image = validated_data.get('image', instance.image)
            instance.save()
            return instance


class Messageserializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False)
    class Meta:
        model = Message
        fields = ('sender', 'chat', 'text')
    


