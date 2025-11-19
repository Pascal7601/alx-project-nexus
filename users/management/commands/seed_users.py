from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random
import faker
User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with random users"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of users to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        fake = faker.Faker()
        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            password = 'password123'  # Default password for all seeded users
            role = random.choice([User.Roles.CANDIDATE, User.Roles.RECRUITER])
            User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} users'))