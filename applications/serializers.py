from rest_framework import serializers
from .models import Application
from jobs.serializers import JobPostingReadSerializer
from users.serializers import CandidateProfileSerializer


class CandidateApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for a candidate's application overview.
    """
    job = JobPostingReadSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'status', 'applied_at']

class ApplicationReadSerializer(serializers.ModelSerializer):
    """
    Serializer for READING applications.
    Includes nested details so the frontend doesn't need extra API calls.
    """
    # Nest the Job details (for the Candidate's dashboard)
    job = JobPostingReadSerializer(read_only=True)
    
    # Nest the Candidate details (for the Recruiter's dashboard)
    candidate = CandidateProfileSerializer(read_only=True)
    match_score = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 
            'job', 
            'candidate', 
            'status', 
            'applied_at',
            'match_score'
        ]
    
    def get_match_score(self, obj):
        """
        Calculate and return the match score between the candidate's skills
        and the job's required skills as a percentage.
        """
        job_skills = set(obj.job.required_skills.values_list('id', flat=True))
        candidate_skills = set(obj.candidate.skills.values_list('id', flat=True))

        if not job_skills:
            return 0.0

        matched_skills = job_skills.intersection(candidate_skills)
        match_percentage = (len(matched_skills) / len(job_skills)) * 100
        return round(match_percentage, 2)

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