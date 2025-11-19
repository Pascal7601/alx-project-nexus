from django.core.management.base import BaseCommand
from skills.models import Skill
import random
import faker

class Command(BaseCommand):
    help = "Seed the database with random skills"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of skills to create'
        )

    def handle(self, *args, **options):
        count = options['count']
        fake = faker.Faker()
        for _ in range(count):
            name = fake.unique.word().capitalize()
            Skill.objects.create(name=name)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} skills'))