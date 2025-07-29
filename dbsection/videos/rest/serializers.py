from rest_framework import serializers

from dbsection.users.models import AppUser
from dbsection.users.rest.serializers import AppUserPreviewSerializer
from dbsection.videos.models import Video, VideoFile


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