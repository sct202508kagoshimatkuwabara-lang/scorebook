from django.contrib import admin
from .models import Game, Lineup, Inning

@admin.register(Lineup)
class LineupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_id_display",
        "team",
        "batting_order",
        "player",
        "position",
    )
    list_filter = ("game", "team", "position")
    search_fields = ("player__name",)

    @admin.display(description="Game ID")
    def game_id_display(self, obj):
        return obj.game_id


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
        "get_top_bottom",
        "runs",
        "outs",
        "current_batter",
    )
    list_filter = ("game", "number", "is_top")
    
    # get_top_bottom メソッドを追加して、'表' / '裏' を表示
    def get_top_bottom(self, obj):
        return '表' if obj.is_top else '裏'
    get_top_bottom.short_description = '表/裏'  # 表示名のカスタマイズ
