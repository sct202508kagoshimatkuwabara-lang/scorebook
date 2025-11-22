from django.db import models

class Player(models.Model):
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

    # Team は teams アプリにあるので "teams.Team"
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="players"
    )

    name = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    jersey_number = models.PositiveIntegerField(null=True, blank=True)
    default_position = models.IntegerField(choices=POSITION_CHOICES, null=True, blank=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}（{self.team.name}）"
