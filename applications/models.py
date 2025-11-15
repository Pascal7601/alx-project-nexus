from django.db import models
from uuid import uuid4
from jobs.models import JobPosting
from users.models import CandidateProfile


class Application(models.Model):
    """Application table to store details of candidates 
        who've applied for jobs and jobs that thyve applied
    """
    class Status(models.TextChoices):
        APPLIED = "Applied"
        UNDER_REVIEW = "Under Review"
        REJECTED = "Rejected"
        INTERVIEW = "Interview"
        OFFERED = "Offered"


    id = models.UUIDField(default=uuid4, primary_key=True, null=False, blank=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)
    applied_at = models.DateTimeField(auto_now_add=True)

    #relationships
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(JobPosting, related_name="applications", on_delete=models.CASCADE)

    class Meta:
        # store a field with unique candidate and job together to avoid candidate applying several times
        constraints = [
            models.UniqueConstraint(fields=["candidate", "job"], name="unique_application")
        ]
        
    def __str__(self):
        return f"{self.candidate.user.email} -> {self.job.title}"
