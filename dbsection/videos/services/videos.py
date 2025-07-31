from typing import Iterable

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.request import Request

from videos.models import Video
from videos.repositories.videos import IVideoRepository


class VideoService:
    def __init__(self, video_repo: IVideoRepository):
        self.video_repo = video_repo


    def get_visible_videos(self, user: User | None = None) -> Iterable[Video]:
        if user and user.is_staff:
            return self.video_repo.get_all_videos()

        visible_videos = self.video_repo.get_published()

        if user and user.is_authenticated:
            visible_videos = visible_videos | self.video_repo.get_by_owner(user=user)
            visible_videos = visible_videos.distinct()

        return visible_videos


    def get_video_with_access_check(
            self,
            video_id: int,
            user: User | None = None
    ) -> Video | None:
        video = self.video_repo.get_video_by_id(video_id=video_id)
        if not video:
            return None

        if (
                video.is_published == Video.StatusChoices.PUBLISHED
                or (user and user.is_staff)
                or (user and user.is_authenticated == video.owner)
        ):
            return video

        return None


    def get_published_video_ids(self) -> Iterable[int]:
        return self.video_repo.get_published_ids()


    def get_stats_with_subquery(self) -> Iterable[Video]:
        return self.video_repo.get_stats_with_subquery()


    def get_stats_with_groupby(self) -> Iterable[Video]:
        return self.video_repo.get_stats_with_groupby()



