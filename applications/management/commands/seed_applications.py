from django.core.management.base import BaseCommand
from applications.models import Application
import random
from faker import Faker
from jobs.models import JobPosting
from django.contrib.auth import get_user_model
User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with random job applications"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of job applications to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker()
        
        all_jobs = list(JobPosting.objects.all())
        all_users = list(User.objects.filter(role=User.Roles.CANDIDATE))
        
        if not all_jobs:
            self.stdout.write(self.style.ERROR('No job postings found! Please seed jobs first.'))
            return
        
        if not all_users:
            self.stdout.write(self.style.ERROR('No candidate users found! Please seed users first.'))
            return

        self.stdout.write(f"Creating {count} job applications...")

        created_count = 0
        for _ in range(count):
            job = random.choice(all_jobs)
            user = random.choice(all_users)
            
            app, created = Application.objects.get_or_create(
                job=job,
                candidate=user.candidate_profile
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} job applications'))