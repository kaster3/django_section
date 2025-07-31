from videos.repositories.likes import ILikeRepository
from videos.repositories.videos import IVideoRepository


class LikeService:
    def __init__(
            self,
            like_repo: ILikeRepository,
            video_repo: IVideoRepository
    ):
        self._like_repo = like_repo
        self._video_repo = video_repo

    def like(self, user_id: int, video_id: int) -> bool:
        if not self._like_repo.create_like(user_id, video_id):
            return False

        self._video_repo.increment_likes(video_id)
        return True

    def unlike(self, user_id: int, video_id: int) -> bool:
        if not self._like_repo.delete_like(user_id, video_id):
            return False

        self._video_repo.decrement_likes(video_id)
        return True