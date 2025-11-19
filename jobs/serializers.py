from rest_framework import serializers
from .models import JobPosting
from skills.serializers import SkillSerializer

class JobPostingReadSerializer(serializers.ModelSerializer):
    """Serializer for the JobPosting model, including nested skills."""
    required_skills = SkillSerializer(many=True, read_only=True)
    
    company_name = serializers.ReadOnlyField(source='company.name')
    company_logo = serializers.ImageField(source='company.logo', read_only=True)
    company_id = serializers.ReadOnlyField(source='company.id')

    class Meta:
        model = JobPosting
        fields = [
            "id", 
            "title", 
            "description", 
            "location", 
            "required_skills",
            "posted_at",
            "updated_at", 
            "is_external", 
            "external_url", 
            "company_name",
            "company_logo",
            "company_id"
        ]

class JobPostingWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating JobPosting without nested skills."""

    class Meta:
        model = JobPosting
        fields = ["title", "description", "location", "required_skills", "is_external", "external_url", "company"]