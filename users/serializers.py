from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CandidateProfile, Company

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "username", "role"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """serialize data from the Post request and save the new user in the db"""
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data.get("username"),
            role=validated_data.get("role", "candidate")
        )
        return user

class CandidateProfileSerializer(serializers.ModelSerializer):
    """serializer of the candidate profile"""
    class Meta:
        model = CandidateProfile
        fields = ["headline", "bio", "location", "skills"]

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "id", "role","first_name", "last_name", "created_at"]

class CompanyReadSerializer(serializers.ModelSerializer):
    """
    Serializer used for GET requests (List/Retrieve).
    Shows the company's public details.
    """
    # Shows the owner's email
    owner_email = serializers.ReadOnlyField(source='owner.email') 

    class Meta:
        model = Company
        fields = [
            'id', 
            'name', 
            'description', 
            'website', 
            'logo', 
            'owner_email'
        ]
        read_only_fields = ['owner_email']


class CompanyWriteSerializer(serializers.ModelSerializer):
    """
    Serializer used for POST/PUT/PATCH requests (Create/Update).
    """
    class Meta:
        model = Company
        # Fields that the user is allowed to send:
        fields = [
            'id', 
            'name', 
            'description', 
            'website', 
            'logo'
        ]
        read_only_fields = ['id']



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'password', 'groups', 'is_staff']