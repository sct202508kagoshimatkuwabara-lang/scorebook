from django.db import models
from apps.teams.models import Team


class Game(models.Model):
    # 大会名（自由入力）
    tournament = models.CharField(
        max_length=100,
        verbose_name="大会名",
        blank=True,
        null=True
    )

    # 試合日時
    game_datetime = models.DateTimeField(
        verbose_name="試合日時"
    )

    # 球場名
    ballpark = models.CharField(
        max_length=100,
        verbose_name="球場名",
        blank=True,
        null=True
    )

    # 天候（選択肢）
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

    # 先攻チーム
    first_batting = models.ForeignKey(
        Team,
        related_name="first_batting_games",
        on_delete=models.CASCADE,
        verbose_name="先攻チーム"
    )

    # 後攻チーム
    second_batting = models.ForeignKey(
        Team,
        related_name="second_batting_games",
        on_delete=models.CASCADE,
        verbose_name="後攻チーム"
    )

    class Meta:
        verbose_name = "試合"
        verbose_name_plural = "試合一覧"

    def __str__(self):
        return f"{self.game_datetime} {self.first_batting} vs {self.second_batting}"
