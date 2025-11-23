from django.contrib import admin
from .models import Team

# Teamモデルを管理画面に表示するクラス
# list_display に表示したいフィールドを指定
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_home_team')
