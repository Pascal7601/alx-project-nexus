from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CandidateProfile

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "username", "role"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data.get("username"),
            role=validated_data.get("role", "candidate")
        )
        return user

class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = ["headline", "bio", "location", "skills"]

class UserDetailSerializer(serializers.ModelSerializer):
    profile = CandidateProfileSerializer()
    class Meta:
        model = User
        fields = ["email", "id", "role","first_name", "last_name", "created_at", "profile"]

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'password', 'groups', 'is_staff']