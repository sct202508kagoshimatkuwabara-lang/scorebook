from django.apps import AppConfig


class GamesConfig(AppConfig):
    name = "apps.games"

    def ready(self):
        pass
        # import apps.games.signals
