from rest_framework import mixins, viewsets

from videos.models import Video


class VideoViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Video.objects.all()
