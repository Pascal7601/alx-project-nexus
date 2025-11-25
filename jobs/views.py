from rest_framework import generics, exceptions
from . import serializers
from .models import JobPosting
from users.permissions import IsRecruiter, IsCompanyOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class JobListCreateView(generics.ListCreateAPIView):
    """GET: List all job postings
       POST: Create a new job posting (Recruiters only)
    """
    serializer_class = serializers.JobPostingReadSerializer
    queryset = JobPosting.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter

    @method_decorator(cache_page(60*15))  # Cache for 15 minutes
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsRecruiter()]
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.JobPostingWriteSerializer
        return serializers.JobPostingReadSerializer
    
    def perform_create(self, serializer):
        """
        Ensure the recruiter owns the company they are posting for.
        """
        # Get the company object from the request data
        company = serializer.validated_data.get('company')

        # Check ownership
        if not company:
            raise exceptions.ValidationError("Company is required.")
            
        if company.owner != self.request.user:
            raise exceptions.PermissionDenied("You can only post jobs for companies you own.")

        serializer.save()
    
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET: Retrieve a job posting
       PUT/PATCH: Update a job posting (Recruiter & Company Owner only)
       DELETE: Delete a job posting (Recruiter & Company Owner only)
    """
    serializer_class = serializers.JobPostingReadSerializer
    queryset = JobPosting.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsRecruiter(), IsCompanyOwner()]
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.JobPostingWriteSerializer
        return serializers.JobPostingReadSerializer
