from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # ホームは scores の home
    path("", include("scores.urls")),

    # チーム管理
    path("teams/", include("teams.urls")),

    # 選手管理
    path("players/", include("players.urls")),
]
