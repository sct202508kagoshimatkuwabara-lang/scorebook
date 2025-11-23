from django.contrib import admin
from .models import Team, Game
from apps.players.models import Player


# --- Inline Settings ---

class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('game_date', 'team_home', 'team_away', 'first_batting')
    list_filter = ('game_date', 'team_home', 'team_away')
