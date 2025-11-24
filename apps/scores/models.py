from django.db import models
from apps.games.models import Game, Lineup

class Pitch(models.Model):
    """
    1球ごとの記録。
    1球＝1レコードになるイメージ。
    """
    game = models.ForeignKey(
        Game,
        related_name="pitches",
        on_delete=models.CASCADE
    )

    # 今どの打順を記録しているか（1〜9）
    batting_order = models.PositiveSmallIntegerField()

    # この打席の打者（Lineup から取得）
    hitter = models.ForeignKey(
        Lineup, on_delete=models.CASCADE, null=True, blank=True
    )

    # 投球結果（BALL / STRIKE / FOUL / INPLAY / HIT など）
    pitch_result = models.CharField(
        max_length=20,
        choices=[
            ("ball", "ボール"),
            ("strike", "ストライク"),
            ("foul", "ファウル"),
            ("inplay", "インプレー"),
            ("hit", "ヒット"),
            ("out", "アウト"),
        ]
    )

    # 打席が終了したときだけ埋まる「最終結果」
    # （三振、四球、ゴロアウト、内野安打、二塁打など）
    atbat_result = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # どの投球番号か（1球目＝1）
    pitch_number = models.PositiveIntegerField()

    # 回（1〜9） ※ 途中延長は必要に応じて増やす
    inning = models.PositiveIntegerField(default=1)

    # 表 or 裏
    top_bottom = models.CharField(
        max_length=6,   # ← 修正！
        choices=[
            ("top", "表"),
            ("bottom", "裏"),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["game", "inning", "pitch_number"]

    def __str__(self):
        return f"{self.game} {self.inning}回{self.top_bottom} {self.pitch_number}球"
