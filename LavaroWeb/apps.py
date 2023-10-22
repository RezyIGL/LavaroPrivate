from django.apps import AppConfig


class LavarowebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LavaroWeb'

    def ready(self) -> None:
        import LavaroWeb.signals
