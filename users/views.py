from rest_framework import generics, status
from . import serializers
from utils import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import CandidateProfile, Company
from .permissions import IsCompanyOwner, IsRecruiter

class UserCreateView(generics.CreateAPIView):
    """
    registers a new user on the db and returns a success response
    """
    serializer_class = serializers.UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny] #Allow anyone to register

    def create(self, request, *args, **kwargs):
        """serialize the data, save the user  and manually return a custom response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {
            "message": f"Your account has been succesfully created",
            "user_details": {
                "id": f"{user.id}",
                "email": f"{user.email}",
                "role": f"{user.role}"
            }
        }
        return Response(response, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveAPIView):
    """returns the details of the current logged in user"""
    serializer_class = serializers.UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated] #allow only authenticated users to view their profile

    def get_object(self):
        """return the user that authenticated using the acces token"""
        return self.request.user

class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """returns the profile of the candidate"""
    serializer_class = serializers.CandidateProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = CandidateProfile.objects.all()

    def get_object(self):
        return self.request.user.profile
    
class CompanyListCreateView(generics.ListCreateAPIView):
    """
    GET: List all companies (public)
    POST: Create a new company (recruiter only)
    """
    # We use the read serializer for the list action
    serializer_class = serializers.CompanyReadSerializer
    queryset = Company.objects.all()
    
    # We use multiple permission classes here, 
    # but the view only needs to be authenticated for POST.
    permission_classes = [AllowAny] 

    def get_serializer_class(self):
        """
        Dynamically use the WriteSerializer for POST requests.
        """
        if self.request.method == 'POST':
            return serializers.CompanyWriteSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Override to automatically set the 'owner' field to the current user
        and prevent Candidates from creating companies.
        """
        # Check if the user is a recruiter before creating (Enforcing POST permission)
        if not self.request.user.is_authenticated or self.request.user.role != 'recruiter':
            self.permission_denied(self.request, message="Only recruiters can create a company.")

        # Save the company and automatically set the owner
        serializer.save(owner=self.request.user)
        
        
class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single company (public)
    PUT/PATCH: Update a company (owner only)
    DELETE: Delete a company (owner only)
    """
    queryset = Company.objects.all()
    serializer_class = serializers.CompanyReadSerializer
    
    # We allow anyone to view, but only the owner to edit/delete
    permission_classes = [IsCompanyOwner]


    def get_serializer_class(self):
        """
        Dynamically use the WriteSerializer for update methods.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.CompanyWriteSerializer
        return self.serializer_class