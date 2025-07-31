from dependency_injector import containers, providers

from .repositories.likes import DjangoLikeRepository
from .repositories.videos import DjangoVideoRepository
from .services.likes import LikeService
from .services.videos import VideoService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "videos.rest.views",
    ])

    video_repo = providers.Factory(
        DjangoVideoRepository
    )

    like_repo = providers.Factory(
        DjangoLikeRepository
    )

    like_service = providers.Factory(
        LikeService,
        like_repo=like_repo,
        video_repo=video_repo
    )

    video_service = providers.Factory(
        VideoService,
        video_repo=video_repo
    )