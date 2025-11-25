# apps/games/admin.py
from django.contrib import admin
from .models import Game, Lineup, Inning


@admin.register(Lineup)
class LineupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game",
        "team",
        "batting_order",
        "player",
        "position",
    )
    list_filter = ("game", "team", "position")
    search_fields = ("player__name",)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_datetime",
        "tournament",
        "first_batting",
        "second_batting",
    )
    list_filter = ("game_datetime", "first_batting", "second_batting")
    search_fields = ("tournament",)

@admin.register(Inning)
class InningAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game",
        "number",
        "is_top",
        "top_bottom",
        "runs",
        "outs",
        "current_batter",
    )
    list_filter = ("game", "number", "is_top")
