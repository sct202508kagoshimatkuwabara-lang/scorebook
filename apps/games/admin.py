from .models import Game
from django.contrib import admin

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "game_datetime", "tournament", "ballpark",
                    "first_batting", "second_batting", "weather")
    list_filter = ("tournament", "ballpark", "weather")
    search_fields = ("tournament",)