from rest_framework import serializers
from .models import Application
from jobs.serializers import JobPostingReadSerializer
from users.serializers import CandidateProfileSerializer

class ApplicationReadSerializer(serializers.ModelSerializer):
    """
    Serializer for READING applications.
    Includes nested details so the frontend doesn't need extra API calls.
    """
    # Nest the Job details (for the Candidate's dashboard)
    job = JobPostingReadSerializer(read_only=True)
    
    # Nest the Candidate details (for the Recruiter's dashboard)
    candidate = CandidateProfileSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 
            'job', 
            'candidate', 
            'status', 
            'applied_at'
        ]

class ApplicationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for CREATING an application.
    """
    class Meta:
        model = Application
        fields = ['id', 'status'] # Status defaults to 'Applied'
        read_only_fields = ['id', 'status']

class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for RECRUITERS to update status.
    """
    class Meta:
        model = Application
        fields = ['status']