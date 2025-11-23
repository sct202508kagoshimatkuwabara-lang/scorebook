from django.db import models

class Player(models.Model):
    # --- ポジション選択肢 ---
    # Django の choices は (DBに保存される値, 表示名) のペアで定義する
    POSITION_CHOICES = [
        (1, "投手"),
        (2, "捕手"),
        (3, "一塁手"),
        (4, "二塁手"),
        (5, "三塁手"),
        (6, "遊撃手"),
        (7, "左翼手"),
        (8, "中堅手"),
        (9, "右翼手"),
    ]

    # --- 所属チーム ---
    # Team は teams アプリにあるので apps 名を含む文字列参照を使用
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,   # チーム削除 → 選手も削除
        related_name="players"      # team.players で選手一覧を取得
    )

    # --- 選手名 ---
    name = models.CharField(max_length=50)

    # --- 生年月日（任意入力） ---
    birthday = models.DateField(null=True, blank=True)

    # --- 背番号（任意入力） ---
    jersey_number = models.PositiveIntegerField(null=True, blank=True)

    # --- デフォルトポジション（任意入力） ---
    default_position = models.IntegerField(
        choices=POSITION_CHOICES,
        null=True,
        blank=True
    )

    # --- コメント（任意入力 / メモ欄） ---
    comment = models.TextField(blank=True)

    # --- 管理画面や一覧での表示 ---
    class Meta:
        verbose_name = "選手"
        verbose_name_plural = "選手一覧"

    def __str__(self):
        # 例：大谷翔平（北海道日本ハムファイターズ）
        return f"{self.name}（{self.team.name}）"
