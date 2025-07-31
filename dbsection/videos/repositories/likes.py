
from typing import Protocol

from django.db import IntegrityError, transaction

from videos.models import Like


from abc import abstractmethod


class ILikeRepository(Protocol):
    @abstractmethod
    def create_like(self, user_id: int, video_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_like(self, user_id: int, video_id: int) -> bool:
        raise NotImplementedError


class DjangoLikeRepository(ILikeRepository):
    def create_like(self, user_id: int, video_id: int) -> bool:
        try:
            with transaction.atomic():
                Like.objects.create(user_id=user_id, video_id=video_id)
            return True
        except IntegrityError:
            return False

    def delete_like(self, user_id: int, video_id: int) -> bool:
        with transaction.atomic():
            deleted, _ = Like.objects.filter(
                user_id=user_id,
                video_id=video_id
            ).delete()
            return bool(deleted)