from rest_framework import serializers

from users.models import AppUser
from users.rest.serializers import AppUserPreviewSerializer
from videos.models import Video, VideoFile


class VideoRetrieveFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ("file", "quality")


class VideoRetrieveSerializer(serializers.ModelSerializer):
    owner = AppUserPreviewSerializer()
    files = VideoRetrieveFileSerializer(many=True)

    class Meta:
        model = Video
        fields = ("pk", "owner", "files", "name", "total_likes", "created_at")


class StatisticsSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    likes_sum = serializers.IntegerField()

    class Meta:
        model = AppUser
        fields = ("username", "likes_sum")