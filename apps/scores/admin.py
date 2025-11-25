from django.contrib import admin
from .models import Pitch


@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game",
        "inning",
        "top_bottom",
        "pitch_number",

        # 守備9人
        "pitcher",
        "catcher",
        "first",
        "second",
        "third",
        "short",
        "left",
        "center",
        "right",

        # 打者
        "hitter",
        "batting_order",

        # 結果
        "pitch_result",
        "atbat_result",

        # ランナー3人
        "runner_1b",
        "runner_2b",
        "runner_3b",

        "created_at",
    )

    list_filter = (
        "game",
        "inning",
        "top_bottom",
        "pitcher",
        "hitter",
    )

    search_fields = (
        "hitter__player__name",
        "pitcher__name",
    )
