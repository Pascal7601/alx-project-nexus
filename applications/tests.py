from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from utils import User
from .models import Application
from users.models import CandidateProfile, Company
from jobs.models import JobPosting

class ApplicationTests(APITestCase):
    """
    Test suite for the Application endpoints.
    """

    def setUp(self):

        # create recruiter and job posting
        self.recruiter = User.objects.create_user(
            username='recruiteruser',
            password='recruiterpassword123',
            email='recruit@gmail.com',
            role='recruiter'
        )
        self.company = Company.objects.get(owner=self.recruiter)
        self.job_posting = JobPosting.objects.create(
            title='Software Engineer',
            description='Develop and maintain software applications.',
            location='Remote',
            company=self.company,
        )
        # Create candidate A
        self.candidate = User.objects.create_user(
            username='candidateuser',
            password='candidatepassword123',
            email='candidate1@gmail.com'
        )
    
    def test_candidate_can_apply_to_job_posting(self):
        """
        Ensure that a candidate can apply to a job posting.
        """
        self.client.force_authenticate(user=self.candidate)
        url = reverse('apply-job', kwargs={'job_id': self.job_posting.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.first().status, 'Applied')

    def test_candidate_cannot_apply_twice_to_same_job_posting(self):
        """
        Ensure that a candidate cannot apply twice to the same job posting.
        """
        self.client.force_authenticate(user=self.candidate)
        url = reverse('apply-job', kwargs={'job_id': self.job_posting.id})

        # First application
        response1 = self.client.post(url)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Second application
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_non_candidate_cannot_apply_to_job_posting(self):
        """
        Ensure that a non-candidate user cannot apply to a job posting.
        """
        self.client.force_authenticate(user=self.recruiter)
        url = reverse('apply-job', kwargs={'job_id': self.job_posting.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)