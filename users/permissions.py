from rest_framework import permissions
from .models import Company

class IsRecruiter(permissions.BasePermission):
    """
    Only allows users with the 'recruiter' role to proceed.
    """
    message = "You must be a Recruiter to perform this action."

    def has_permission(self, request, view):
        # A user must be authenticated and have the 'recruiter' role
        if not request.user.is_authenticated:
            return False
        
        return request.user.role == 'recruiter'

class IsCompanyOwner(permissions.BasePermission):
    """
    Only allows the owner of the Company to perform action.
    """
    message = "You do not have permission to modify this object."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the object is the Company itself
        if hasattr(obj, 'owner') and not hasattr(obj, 'company'):
            return obj.owner == request.user

        #Check if the object is a JobPosting (which is linked to a company)
        if hasattr(obj, 'company'):
            # Safety check: The job might be a scraped one (no company)
            if obj.company is None:
                return False 
            
            # Does the User own the Company that owns this Job?
            return obj.company.owner == request.user
        
        return False