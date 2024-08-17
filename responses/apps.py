from django.apps import AppConfig


class ResponsesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "responses"

    def ready(self) -> None:
        from responses import signals

        return super().ready()
