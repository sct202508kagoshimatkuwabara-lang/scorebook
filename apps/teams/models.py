from django.db import models

class Team(models.Model):
    # 球団名（例：北海道日本ハムファイターズ）
    name = models.CharField(max_length=100)

    # 本拠地（例：北海道（エスコンフィールドHOKKAIDO））
    location = models.CharField(max_length=200)

    # デフォルトのホーム（運営）チームかどうか
    # True のチームがアプリ内の「ホーム扱い」になる
    is_home_team = models.BooleanField(default=False)

    class Meta:
        verbose_name = "チーム"
        verbose_name_plural = "チーム一覧"

    def __str__(self):
        # 管理画面などで表示するときの名称
        return self.name
