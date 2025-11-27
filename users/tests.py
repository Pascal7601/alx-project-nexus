from django.test import TestCase
from unittest.mock import patch
from utils import User
from .models import CandidateProfile, Company

class UserSignalTests(TestCase):
    """
    Tests that profiles are created when user is created
    """

    @patch('users.tasks.send_verification_email.delay')
    def test_candidate_profile_creation(self, mock_celery):

        # Create a new user
        user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpassword123',
            role='candidate'
        )
        # Check that a CandidateProfile was created
        self.assertTrue(CandidateProfile.objects.filter(user=user).exists())

        #Assert that company does not exist for this user
        self.assertFalse(Company.objects.filter(owner=user).exists())
        
    
    @patch('users.tasks.send_verification_email.delay')
    def test_company_creation_for_recruiter(self, mock_celery):

        # Create a new recruiter user
        user = User.objects.create_user(
            username='recruiteruser',
            email='recruit@gmail.com',
            password='recruiterpassword123',
            role='recruiter'
        )
        # Assert that Company exists for this user
        self.assertTrue(Company.objects.filter(owner=user).exists())

        # Assert that CandidateProfile does not exist for this user
        self.assertFalse(CandidateProfile.objects.filter(user=user).exists())