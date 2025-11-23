from django import forms
from apps.teams.models import Team  # ← これだけでOK

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'location']   # ← location を追加

