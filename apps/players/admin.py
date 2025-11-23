from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "team", "jersey_number", "default_position")
    list_filter = ("team", "default_position")
    search_fields = ("name",)
