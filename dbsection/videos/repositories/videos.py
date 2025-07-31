from abc import abstractmethod
from typing import Protocol, Iterable

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import F, QuerySet, OuterRef, Sum, Subquery, Count

from videos.models import Video


class IVideoRepository(Protocol):
    @abstractmethod
    def get_video_by_id(self, video_id: int) -> Video | None:
        raise NotImplementedError

    @abstractmethod
    def get_all_videos(self) -> Iterable[Video]:
        raise NotImplementedError

    @abstractmethod
    def get_published(self) -> Iterable[Video]:
        raise NotImplementedError

    @abstractmethod
    def get_by_owner(self, owner: User) -> Iterable[Video]:
        raise NotImplementedError

    @abstractmethod
    def get_published_ids(self) -> Iterable[int]:
        raise NotImplementedError

    @abstractmethod
    def get_stats_with_subquery(self) -> Iterable[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_stats_with_groupby(self) -> Iterable[dict]:
        raise NotImplementedError

    @abstractmethod
    def increment_likes(self, video_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def decrement_likes(self, video_id: int) -> None:
        raise NotImplementedError




class DjangoVideoRepository(IVideoRepository):
    def get_video_by_id(self, video_id: int) -> Video | None:
        try:
            return Video.objects.select_related("owner").prefetch_related("files").get(pk=video_id)
        except Video.DoesNotExist:
            return None

    def get_all_videos(self) -> QuerySet[Video]:
        return Video.objects.select_related("owner").prefetch_related("files").all()

    def get_published(self) -> QuerySet[Video]:
        return (
            Video.objects
            .filter(is_published=Video.StatusChoices.PUBLISHED)
            .select_related("owner")
            .prefetch_related("files")
        )

    def get_by_owner(self, owner: User) -> QuerySet[Video]:
        return (
            Video.objects
            .filter(owner=owner)
            .select_related("owner")
            .prefetch_related("files")
        )

    def increment_likes(self, video_id: int) -> None:
        Video.objects.filter(pk=video_id).update(
            total_likes=F("total_likes") + 1
        )

    def decrement_likes(self, video_id: int) -> None:
        Video.objects.filter(pk=video_id).update(
            total_likes=F("total_likes") - 1
        )

    def get_published_ids(self) -> QuerySet[int]:
        return (
            Video.objects.
            filter(is_published=Video.StatusChoices.PUBLISHED).
            values_list("id", flat=True).
            order_by("id")
        )

    def get_stats_with_subquery(self) -> QuerySet[dict]:
        user = get_user_model()
        subquery = (
            self.get_published()
            .filter(owner=OuterRef("pk"))
            .values("owner")
            .annotate(likes_sum=Sum("total_likes"))
            .values("likes_sum")
        )
        return (
            user.objects
            .annotate(likes_sum=Subquery(subquery))
            .values("username", "likes_sum")
            .order_by("-likes_sum")
        )

    def get_stats_with_groupby(self) -> QuerySet[dict]:
        return (
            self.get_published()
            .values("owner__username")
            .annotate(
                username=F("owner__username"),
                likes_sum=Sum("total_likes")
            )
            .values("username", "likes_sum")
            .order_by("-likes_sum")
        )

