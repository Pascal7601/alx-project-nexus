from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from utils import User
from .models import JobPosting
from users.models import Company


class JobPostingTests(APITestCase):
    """
    Test suite for the JobPosting endpoints.
    """

    def setUp(self):
        # Create  recruiter A
        self.recruiter = User.objects.create_user(
            username='recruiteruser',
            email='recruit@gmail.com',
            password='recruiterpassword123',
            role='recruiter',
        )
        self.company_a = Company.objects.get(owner=self.recruiter)

        # create a job posting
        self.job_posting = JobPosting.objects.create(
            title='Software Engineer',
            description='Develop and maintain software applications.',
            location='Remote',
            company=self.company_a,
        )

        # Create recruiter B
        self.other_recruiter = User.objects.create_user(
            username='otherrecruiter',
            email='otherrecruit@gmail.com',
            password='otherrecruiterpassword123',
            role='recruiter',
        )
        self.company_b = Company.objects.get(owner=self.other_recruiter)

        # create a candidate (unauthorized user for job posting)
        self.candidate = User.objects.create_user(
            username='candidateuser',
            email='candidate@gmail.com',
            password='candidatepassword123',
            role='candidate',
        )

    def test_candidate_cannot_create_job_posting(self):
        """
        Ensure that a candidate cannot create a job posting.
        """
        self.client.force_authenticate(user=self.candidate)
        url = reverse('job-list-create')
        data = {
            'title': 'Data Scientist',
            'description': 'Analyze and interpret complex data.',
            'location': 'New York, NY',
            'company': self.company_a.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_recruiter_cannot_post_for_other_company(self):
        """
        Ensure that a recruiter cannot post a job for a company they do not own.
        """
        self.client.force_authenticate(user=self.other_recruiter)
        url = reverse('job-list-create')
        data = {
            'title': 'Product Manager',
            'description': 'Oversee product development lifecycle.',
            'location': 'San Francisco, CA',
            'company': self.company_a.id,  # Company owned by recruiter A
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_recruiter_can_create_job_posting(self):
        """
        Ensure that a recruiter can create a job posting for their own company.
        """
        self.client.force_authenticate(user=self.recruiter)
        url = reverse('job-list-create')
        data = {
            'title': 'Frontend Developer',
            'description': 'Build and optimize user interfaces.',
            'location': 'Austin, TX',
            'company': self.company_a.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Frontend Developer')