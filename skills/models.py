from django.db import models
from uuid import uuid4

class Skill(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid4)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"
