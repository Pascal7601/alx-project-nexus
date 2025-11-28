from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from uuid import uuid4

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """implement creating a new user using an email and password"""
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    User model with roles such as candidate and company
    """
    class Roles(models.TextChoices):
        CANDIDATE = "candidate"
        RECRUITER = "recruiter"

    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid4)
    email = models.EmailField(max_length=254, null=False, unique=True)
    password = models.CharField(max_length=254, null=False, blank=False)
    username = models.CharField(max_length=254, null=True, blank=True)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Roles, default=Roles.CANDIDATE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    class Meta:
        ordering = ["created_at"]

class CandidateProfile(models.Model):
    """
    candidate profile model that will be generated automatically when
    the user is a candidate
    """
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="candidate_profile"
        )
    headline = models.CharField(max_length=254, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}"
    
    #relationships
    skills = models.ManyToManyField("skills.Skill", blank=True)
    

class Company(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid4)
    name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(max_length=254, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)

    #relationships
    owner = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="companies"
        )

    def __str__(self):
        return f"{self.name}"