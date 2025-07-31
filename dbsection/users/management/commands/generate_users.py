from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Generates test users"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10000, help="Number of users to create")

    def handle(self, *args, **options):
        count = options["count"]
        users = [User(username=f'user_{i}') for i in range(1, count+1)]
        User.objects.bulk_create(users, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"Created {count} users"))