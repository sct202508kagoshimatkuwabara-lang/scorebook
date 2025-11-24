# apps/games/models.py
from django.db import models
from apps.teams.models import Team
from apps.players.models import Player

"""
games アプリのモデル定義（全文）
 - Game: 試合情報（日時・球場・先攻/後攻）
 - Lineup: 1試合・1チームの打順（1〜9番）
 - Inning: イニング（回 + 表裏）
 
注:
 - 投球（Pitch）やイニングの詳細な記録は apps.scores.Pitch 等で扱う想定。
 - apps 配下のモジュールを参照するため imports は apps.<app>.models の形式を使用。
"""

class Game(models.Model):
    # 大会名（任意）
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

    # 球場名（任意）
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

    # 先攻チーム（home/away の概念ではなく「先に打つチーム」）
    first_batting = models.ForeignKey(
        Team,
        related_name="first_batting_games",
        on_delete=models.CASCADE,
        verbose_name="先攻チーム"
    )

    # 後攻チーム（後攻＝2番目に打つチーム）
    second_batting = models.ForeignKey(
        Team,
        related_name="second_batting_games",
        on_delete=models.CASCADE,
        verbose_name="後攻チーム"
    )

    class Meta:
        verbose_name = "試合"
        verbose_name_plural = "試合一覧"
        ordering = ["-game_datetime"]

    def __str__(self):
        # 管理画面などで見やすくするための文字列表示
        return f"{self.game_datetime} {self.first_batting} vs {self.second_batting}"


# --------------------------------------------
# Lineup（打順：1〜9番）
# --------------------------------------------
class Lineup(models.Model):
    """
    1試合・1チームに対する各打者のエントリ（1〜9番）
    - Player.default_position は参考値。実際のその試合での守備位置はここで指定する。
    - unique_together により (game, team, batting_order) がユニークになる。
    """

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

    # Player.POSITION_CHOICES を参照（1〜9 の守備位置）
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


# --------------------------------------------
# Inning（回・表裏）
# --------------------------------------------
class Inning(models.Model):
    """
    イニング情報（1回〜）
    """
    game = models.ForeignKey(
        Game,
        related_name="innings",
        on_delete=models.CASCADE
    )
    number = models.PositiveSmallIntegerField("回")  
    is_top = models.BooleanField("表かどうか", default=True)

    # Pitch と整合させるための文字列フィールド
    top_bottom = models.CharField(
        max_length=10,
        choices=[("top", "表"), ("bottom", "裏")],
        default="top"
    )

    # ←★ ここから追加（超重要）
    runs = models.PositiveSmallIntegerField(default=0)   # 表 or 裏の得点
    outs = models.PositiveSmallIntegerField(default=0)   # アウトカウント
    current_batter = models.PositiveSmallIntegerField(default=1)  # 打順 1〜9

    class Meta:
        verbose_name = "イニング"
        verbose_name_plural = "イニング一覧"
        unique_together = ("game", "number", "is_top")
        ordering = ["game", "number", "is_top"]

    def __str__(self):
        return f"{self.game} {self.number}回{'表' if self.is_top else '裏'}"
