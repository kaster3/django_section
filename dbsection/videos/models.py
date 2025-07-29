from django.db import models


class Video(models.Model):
    class StatusChoices(models.IntegerChoices):
        NOT_PUBLISHED = 0, "Not published video"
        PUBLISHED = 1, "Published video"

    owner = models.ForeignKey("users.AppUser", on_delete=models.PROTECT, related_name="videos")
    name = models.CharField(max_length=255)
    is_published = models.BooleanField(choices=StatusChoices, default=StatusChoices.NOT_PUBLISHED)
    total_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VideoFile(models.Model):
    class QualityChoices(models.TextChoices):
        HD = "HD", "720p"
        FHD = "FHD", "1080p"
        UHD = "UHD", "4K"

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="videos/")
    quality = models.CharField(max_length=3, choices=QualityChoices.choices, default=QualityChoices.HD)

    class Meta:
        unique_together = ("video", "quality")

    def __str__(self):
        return f"{self.video.name} ({self.quality})"

class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("users.AppUser", on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("video", "user")
