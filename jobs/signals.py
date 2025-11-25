from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import JobPosting
from django.core.cache import cache

@receiver([post_save, post_delete], sender=JobPosting)
def invalidate_job_cache(sender, instance, **kwargs):
    """
    Invalidate cache related to JobPosting whenever a job is created, updated, or deleted.
    """
    cache.clear()  # Clear all cache to ensure consistency