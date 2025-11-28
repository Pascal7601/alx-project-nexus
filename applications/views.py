from rest_framework import generics, permissions, exceptions
from . import serializers
from .models import Application
from jobs.models import JobPosting
from users.permissions import IsRecruiter
from django.db import IntegrityError

class ApplyJobView(generics.CreateAPIView):
    """
    POST /api/jobs/<job_id>/apply/
    Allows a logged-in CANDIDATE to apply for a specific job.
    """
    serializer_class = serializers.ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get the Job ID from the URL
        job_id = self.kwargs.get('job_id')
        job = generics.get_object_or_404(JobPosting, id=job_id)

        # Check if it's an external job (Scraper job)
        if job.is_external:
            raise exceptions.ValidationError(
                f"This is an external job. Please apply at {job.external_url}"
            )

        # Get the Candidate Profile
        user = self.request.user
        if user.role != 'candidate':
            raise exceptions.PermissionDenied("Only candidates can apply.")
        
        # Save the application
        try:
            serializer.save(candidate=user.candidate_profile, job=job)
        except IntegrityError:
            raise exceptions.ValidationError("You have already applied for this job.")


class CandidateApplicationListView(generics.ListAPIView):
    """
    GET /api/applications/my/
    Shows a candidate all the jobs they have applied to.
    """
    serializer_class = serializers.ApplicationReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter applications where the candidate is the current user
        return Application.objects.filter(candidate=self.request.user.candidateprofile)


class JobApplicantsListView(generics.ListAPIView):
    """
    GET /api/jobs/<job_id>/applicants/
    Shows a recruiter all applicants for a specific job.
    """
    serializer_class = serializers.ApplicationReadSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        job = generics.get_object_or_404(JobPosting, id=job_id)

        # Does this recruiter own the company that posted this job?
        if job.company.owner != self.request.user:
             raise exceptions.PermissionDenied("You do not have permission to view these applicants.")

        return Application.objects.filter(job=job).select_related(
            'job, candidate',
        ).prefetch_related(
            'job__required_skills',
            'candidate__skills'
        ).order_by('-applied_at')


class ApplicationStatusUpdateView(generics.UpdateAPIView):
    """
    PATCH /api/applications/<pk>/
    Allows a recruiter to update the status (e.g., 'Rejected', 'Interviewing').
    """
    serializer_class = serializers.ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]
    queryset = Application.objects.all()
    http_method_names = ['patch'] # Only allow PATCH

    def perform_update(self, serializer):
        # Security Check: Does the user own the job associated with this application?
        application = self.get_object()
        if application.job.company.owner != self.request.user:
            raise exceptions.PermissionDenied("You cannot update this application.")
        
        serializer.save()