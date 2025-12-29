from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CandidateProfile, Company
from skills.serializers import SkillSerializer
from skills.models import Skill
from utils import User

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "username", "role", "first_name", "last_name"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """serialize data from the Post request and save the new user in the db"""
        user = User.objects.create_user(
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data["email"],
            password=validated_data["password"],
            username=validated_data.get("username"),
            role=validated_data.get("role", "candidate")
        )
        return user

class VerifyEmailSerializer(serializers.Serializer):
    """Serializer for verifying email with a token."""
    token = serializers.CharField()

    def validate(self, attrs):
        """
        Validate the token and inject the user object into validated_data.
        """
        token = attrs.get('token')
        from utils import verify_email_token
        # Verify the token
        user = verify_email_token(token)
        
        if not user:
            raise serializers.ValidationError({"token": "Invalid or expired token."})
        
        attrs['user'] = user
        
        return attrs

class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("User account is not active.")
            return user
        raise serializers.ValidationError("Invalid email or password.")

class CandidateProfileSerializer(serializers.ModelSerializer):
    """serializer of the candidate profile"""
    skills = SkillSerializer(many=True, read_only=True)
    skills_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source='skills',
        queryset=Skill.objects.all()
    )
    class Meta:
        model = CandidateProfile
        fields = ["headline", "bio", "location", "skills", "user", "skills_ids"]

        read_only_fields = ['user']

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