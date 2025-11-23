from django import forms
from .models import Team
from .models import Game

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'location']   # ← location を追加


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["game_date", "team_home", "team_away"]
        widgets = {
            "game_date": forms.DateInput(attrs={"type": "date"}),
        }
