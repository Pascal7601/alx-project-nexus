from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model

User = get_user_model()

class JobPosting(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid4)
    title = models.CharField(max_length=254)
    description = models.TextField()
    location = models.CharField(max_length=254, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_external = models.BooleanField(default=False)
    external_url = models.URLField(max_length=254)

    #relationships
    company = models.ForeignKey(
        "users.Company",
        on_delete=models.CASCADE, null=True, blank=True,
        related_name="jobs"
    )
    required_skills = models.ManyToManyField(
        "skills.Skill", blank=True, related_name="jobs_requiring"
        )

    def __str__(self):
        if self.company:
            return f"{self.title} at {self.company.name}"
        return f"{self.title} (no company)"