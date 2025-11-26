from django.db import models
from apps.teams.models import Team
from apps.players.models import Player
from django.db.models import JSONField

class Game(models.Model):
    tournament = models.CharField(
        max_length=100,
        verbose_name="大会名",
        blank=True,
        null=True
    )

    game_datetime = models.DateTimeField(
        verbose_name="試合日時"
    )

    ballpark = models.CharField(
        max_length=100,
        verbose_name="球場名",
        blank=True,
        null=True
    )

    WEATHER_CHOICES = [
        ("sunny", "晴れ"),
        ("cloudy", "曇り"),
        ("rain", "雨"),
        ("other", "その他"),
    ]
    weather = models.CharField(
        max_length=20,
        choices=WEATHER_CHOICES,
        verbose_name="天候",
        blank=True,
        null=True
    )

    first_batting = models.ForeignKey(
        Team,
        related_name="first_batting_games",
        on_delete=models.CASCADE,
        verbose_name="先攻チーム"
    )

    second_batting = models.ForeignKey(
        Team,
        related_name="second_batting_games",
        on_delete=models.CASCADE,
        verbose_name="後攻チーム"
    )

    lineup_json = models.JSONField(default=dict, blank=True)
    # --------------------------------------------------
    # lineup_json を自動生成（必要なら）
    # --------------------------------------------------
    def build_lineup_json(self):
        """games_lineup テーブルから lineup を生成して返す（dict）"""
        top_team = self.first_batting
        bottom_team = self.second_batting

        top_lineups = self.lineups.filter(team=top_team).order_by("batting_order")
        bottom_lineups = self.lineups.filter(team=bottom_team).order_by("batting_order")

        def convert(lineup_qs):
            return [
                {
                    "order": lu.batting_order,
                    "id": lu.player.id,
                    "name": lu.player.name,
                    "position": lu.position,
                }
                for lu in lineup_qs
            ]

        def find_pitcher(lineup_qs):
            p = lineup_qs.filter(position=1).first()
            if p:
                return {"id": p.player.id, "name": p.player.name, "position": "P"}
            return None

        return {
            "top": {
                "team_id": top_team.id,
                "team_name": top_team.name,
                "batting": convert(top_lineups),
                "pitching": [find_pitcher(top_lineups)] if find_pitcher(top_lineups) else [],
            },
            "bottom": {
                "team_id": bottom_team.id,
                "team_name": bottom_team.name,
                "batting": convert(bottom_lineups),
                "pitching": [find_pitcher(bottom_lineups)] if find_pitcher(bottom_lineups) else [],
            }
        }


class Lineup(models.Model):
    game = models.ForeignKey(
        Game,
        related_name="lineups",
        on_delete=models.CASCADE
    )

    team = models.ForeignKey(
        Team,
        related_name="lineups",
        on_delete=models.CASCADE
    )

    batting_order = models.PositiveSmallIntegerField(
        "打順（1〜9）"
    )

    position = models.IntegerField(
        "守備位置（1〜9）",
        choices=Player.POSITION_CHOICES,
        null=False,
        blank=False
    )

    player = models.ForeignKey(
        Player,
        related_name="lineup_entries",
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "メンバー表（打順）"
        verbose_name_plural = "メンバー表一覧"
        ordering = ["game", "team", "batting_order"]
        unique_together = ("game", "team", "batting_order")

    def __str__(self):
        return f"{self.game} / {self.team} / {self.batting_order}番：{self.player.name}"


class Inning(models.Model):
    game = models.ForeignKey(
        Game,
        related_name="innings",
        on_delete=models.CASCADE
    )
    number = models.PositiveSmallIntegerField("回")
    is_top = models.BooleanField("表かどうか", default=True)

    top_bottom = models.CharField(
        max_length=10,
        choices=[("top", "表"), ("bottom", "裏")],
        default="top"
    )

    runs = models.PositiveSmallIntegerField(default=0)
    outs = models.PositiveSmallIntegerField(default=0)
    current_batter = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "イニング"
        verbose_name_plural = "イニング一覧"
        unique_together = ("game", "number", "is_top")
        ordering = ["game", "number", "is_top"]

    def __str__(self):
        return f"{self.game} {self.number}回{'表' if self.is_top else '裏'}"
