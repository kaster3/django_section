from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...models import Video
import random
from tqdm import tqdm

User = get_user_model()

class Command(BaseCommand):
    help = "Generates test videos data"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=100000, help="Number of videos to create")

    def handle(self, *args, **options):
        user_count = User.objects.count()
        if user_count == 0:
            self.stdout.write(self.style.ERROR("No users found. Create users first."))
            return

        videos = []
        for i in tqdm(range(1, options["count"] + 1), desc="Creating videos"):
            videos.append(Video(
                owner_id=random.randint(1, user_count),  # Используем ID вместо объекта
                name=f"Video {i}",
                is_published=True,
                total_likes=random.randint(0, 1000)
            ))

            if len(videos) % 5000 == 0:
                Video.objects.bulk_create(videos, batch_size=5000)
                videos = []

        if videos:
            Video.objects.bulk_create(videos)

        # Создание видеофайлов (аналогично)
        ...