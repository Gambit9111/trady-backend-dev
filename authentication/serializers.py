from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=4)
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
    

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': ('Email is already in use')})
        return super().validate(attrs)
    

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['username', 'profile_picture']
