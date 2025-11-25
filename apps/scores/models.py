# apps/scores/models.py
from django.db import models
from apps.games.models import Game, Lineup
from apps.players.models import Player


class Pitch(models.Model):
    """
    1球の記録
    """

    # ① 試合
    game = models.ForeignKey(
        Game,
        related_name="pitches",
        on_delete=models.CASCADE
    )

    # ② イニング（1〜）
    inning = models.PositiveSmallIntegerField(default=1)

    # ③ 表 / 裏
    top_bottom = models.CharField(
        max_length=6,
        choices=[
            ("top", "表"),
            ("bottom", "裏"),
        ]
    )

    # ④ 守備9人 ————（投手だけ必須、他は任意）
    pitcher = models.ForeignKey(
        Player,
        related_name="pitcher_pitches",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    catcher = models.ForeignKey(
        Player,
        related_name="catcher_pitches",
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    first = models.ForeignKey(
        Player,
        related_name="first_pitches",
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    second = models.ForeignKey(
        Player,
        related_name="second_pitches",
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    third = models.ForeignKey(
        Player,
        related_name="third_pitches",
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    short = models.ForeignKey(
        Player,
        related_name="short_pitches",
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    left = models.ForeignKey(
        Player,
        related_name="left_pitches",
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    center = models.ForeignKey(
        Player,
        related_name="center_pitches",
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    right = models.ForeignKey(
        Player,
        related_name="right_pitches",
        on_delete=models.PROTECT,
        null=True, blank=True
    )

    # ⑤ 打者（Lineup に紐付く）
    hitter = models.ForeignKey(
        Lineup,
        related_name="hitter_pitches",
        on_delete=models.PROTECT,
        null=False
    )

    # ※ 打順（1〜9）
    batting_order = models.PositiveSmallIntegerField()

    # ⑥ 打者結果（打席終了時にだけ値が入る）
    atbat_result = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    # ⑦ 投球結果
    pitch_result = models.CharField(
        max_length=20,
        choices=[
            ("ball", "ボール"),
            ("strike", "ストライク"),
            ("foul", "ファウル"),
            ("inplay", "インプレー"),
        ]
    )

    # 投球番号（1球目＝1）
    pitch_number = models.PositiveIntegerField()

    # ⑧ ランナー状況
    runner_1b = models.ForeignKey(
        Player, related_name="on_first",
        null=True, blank=True, on_delete=models.SET_NULL
    )
    runner_2b = models.ForeignKey(
        Player, related_name="on_second",
        null=True, blank=True, on_delete=models.SET_NULL
    )
    runner_3b = models.ForeignKey(
        Player, related_name="on_third",
        null=True, blank=True, on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["game", "inning", "pitch_number"]
        verbose_name = "スコア"
        verbose_name_plural = "スコア一覧"

    def __str__(self):
        return f"{self.game} {self.inning}回{self.top_bottom} {self.pitch_number}球"
