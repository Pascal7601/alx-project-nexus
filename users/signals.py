from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CandidateProfile, Company

@receiver(post_save, sender=User)
def create_candidate_profile(sender, instance, created, **kwargs):
    """
    create a signal to automatically create a Candidate profile when the user
    is a candidate and a company profile when the user is a recruiter
    """
    if created:
        if instance.role == "candidate":
            candidate = CandidateProfile(user=instance)
            candidate.save()
        elif instance.role == "recruiter":
            company = Company(owner=instance, name=f"{instance.username}'s company")
            company.save()