from django.core.management.base import BaseCommand
from jobs.models import JobPosting
import random
from faker import Faker
from skills.models import Skill


class Command(BaseCommand):
    help = "Seed the database with random job listings"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of job listings to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker()
        
        # Get all skills into a list so we can sample them
        all_skills = list(Skill.objects.all())
        
        if not all_skills:
            self.stdout.write(self.style.ERROR('No skills found! Please seed skills first.'))
            return

        self.stdout.write(f"Creating {count} jobs...")

        for _ in range(count):
            title = fake.job()
            description = fake.text(max_nb_chars=200)
            location = fake.city()
            
            # Create the Job FIRST (without skills)
            # This saves the job and generates an ID (UUID)
            job = JobPosting.objects.create(
                title=title,
                description=description,
                location=location,
                is_external=True, # Since these have no company, mark them as external/dummy
                external_url=fake.url()
            )
            
            # Add the ManyToMany relationship AFTER the job exists
            num_skills = random.randint(1, min(5, len(all_skills)))
            selected_skills = random.sample(all_skills, k=num_skills)
            
            job.required_skills.set(selected_skills)
