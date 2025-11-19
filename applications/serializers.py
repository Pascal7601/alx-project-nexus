from .models import Application
from rest_framework import serializers
from jobs.serializers import JobPostingReadSerializer

class ApplicationReadSerializer(serializers.ModelSerializer):
    """Serializer for the Application model, including nested job posting details."""

    class Meta:
        model = Application
        fields = [
            "id",
            "applicant_name",
            "applicant_email",
            "resume",
            "cover_letter",
            "applied_at",
            "job"
        ]

class ApplicationWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Application without nested job posting details."""

    class Meta:
        model = Application
        fields = ["applicant_name", "applicant_email", "resume", "cover_letter", "job"]