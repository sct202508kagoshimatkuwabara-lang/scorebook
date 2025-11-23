from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "tournament",
            "game_datetime",
            "ballpark",
            "weather",
            "first_batting",
            "second_batting",
        ]
        widgets = {
            "game_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
