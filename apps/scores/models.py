from django.db import models
from apps.teams.models import Team
from apps.players.models import Player


class Game(models.Model):
    game_date = models.DateField()
    team_home = models.ForeignKey(Team, related_name='games_home', on_delete=models.CASCADE)
    team_away = models.ForeignKey(Team, related_name='games_away', on_delete=models.CASCADE)
    first_batting = models.ForeignKey(Team, related_name='games_first', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.game_date} {self.team_home} vs {self.team_away}"


# AtBat はまだ使わないので、一旦削除して OK
# 必要になったら復活させよう

