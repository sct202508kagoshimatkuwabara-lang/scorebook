from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["team", "name", "birthday", "jersey_number", "default_position", "comment"]
