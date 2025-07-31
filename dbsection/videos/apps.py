from django.apps import AppConfig


class VideosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "videos"

    def ready(self):
        from .containers import Container
        container = Container()
        container.wire(modules=["videos.rest.views"])
