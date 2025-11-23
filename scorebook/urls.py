from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # ホームは scores の home
    path("", include("apps.scores.urls")),

    # チーム管理
    path("teams/", include("apps.teams.urls")),

    # 選手管理
    path("players/", include("apps.players.urls")),
]
