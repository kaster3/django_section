from dependency_injector.wiring import inject, Provide
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import VideoRetrieveSerializer, StatisticsSerializer
from ..containers import Container
from ..services.likes import LikeService
from ..services.videos import VideoService


class VideoPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class VideoViewSet(viewsets.ViewSet):
    pagination_class = VideoPagination

    @inject
    def __init__(
        self,
        video_service: VideoService = Provide[Container.video_service],
        like_service: LikeService = Provide[Container.like_service],
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.like_service = like_service
        self.video_service = video_service

    def list(self, request: Request) -> Response:
        # GET /v1/videos/
        videos = self.video_service.get_visible_videos(user=request.user)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(videos, request)

        serializer = VideoRetrieveSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, pk: int) -> Response:
        # GET /v1/videos/<pk>/
        video = self.video_service.get_video_with_access_check(video_id=pk, user=request.user)

        if not video:
            return Response(
                {"error": "Not found", "detail": f"Video {pk} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VideoRetrieveSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=["POST", "DELETE"], permission_classes=[permissions.IsAuthenticated])
    def likes(self, request: Request, pk: int) -> Response:
        # DELETE /v1/videos/<pk>/likes
        # POST /v1/videos/<pk>/likes
        video = self.video_service.get_video_with_access_check(video_id=pk, user=request.user)

        if not video:
            return Response(
                {"error": "Video not found or access denied"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "POST":
            success = self.like_service.like(user_id=request.user.id, video_id=pk)
            if not success:
                return Response(
                    {"error": "You have already liked this video"},
                    status=status.HTTP_409_CONFLICT
                )
            return Response(status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            success = self.like_service.unlike(user_id=request.user.id, video_id=pk)
            if not success:
                return Response(
                    {"error": "Like not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise NotImplementedError(request.method)

    @action(detail=False, methods=["GET"], permission_classes=[permissions.IsAdminUser])
    def ids(self, request: Request) -> Response:
        # GET /v1/videos/ids/
        published_ids = self.video_service.get_published_video_ids()
        return Response(published_ids, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        url_path="statistics-subquery",
        permission_classes=[permissions.IsAdminUser],
    )
    def statistics_subquery(self, request: Request) -> Response:
        # GET /v1/videos/statistics-subquery/
        stats = self.video_service.get_stats_with_subquery()
        serializer = StatisticsSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=["GET"],
        url_path="statistics-group-by",
        permission_classes=[permissions.IsAdminUser],
    )
    def statistics_group_by(self, request: Request) -> Response:
        # GET /v1/videos/statistics-group-by/
        stats = self.video_service.get_stats_with_groupby()
        serializer = StatisticsSerializer(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)