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
        verbose_name="球場",
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

    def __str__(self):
        return f"{self.tournament} {self.game_datetime.strftime('%Y-%m-%d %H:%M')}"


class Score(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name="試合"
    )

    inning = models.PositiveSmallIntegerField(
        verbose_name="イニング"
    )

    is_top = models.BooleanField(
        verbose_name="表攻撃",
        default=True
    )

    batter = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="batter_scores",
        verbose_name="打者"
    )

    pitcher = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="pitcher_scores",
        verbose_name="投手"
    )

    result = models.CharField(
        max_length=50,
        verbose_name="結果",
        blank=True,
        null=True
    )

    order = models.PositiveSmallIntegerField(
        verbose_name="打席順",
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "スコア"
        verbose_name_plural = "スコア一覧"
        ordering = ["game", "inning", "is_top", "order"]

    def __str__(self):
        return f"{self.game} {self.inning}回{'表' if self.is_top else '裏'} {self.order}番打席"


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
        on_delete=models.CASCADE,
        related_name="innings",
        verbose_name="試合"
    )

    number = models.PositiveSmallIntegerField(
        verbose_name="イニング番号"
    )

    is_top = models.BooleanField(
        verbose_name="表攻撃",
        default=True
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
