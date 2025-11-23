# Django 管理画面
from django.contrib import admin

# path：URLパターン
# include：アプリごとの urls.py を読み込む
from django.urls import path, include

urlpatterns = [
    # 1. Django 標準の管理画面
    path("admin/", admin.site.urls),

    # 2. ホーム画面（TOP ページ）
    #    scores アプリの urls.py の "" (空) を読み込むので、
    #    http://127.0.0.1:8000/ で scores/home が表示される
    path("", include("apps.scores.urls")),

    # 3. チーム管理画面
    #    http://127.0.0.1:8000/teams/
    path("teams/", include("apps.teams.urls")),

    # 4. 選手管理画面
    #    http://127.0.0.1:8000/players/
    path("players/", include("apps.players.urls")),

    # 5. 試合管理（今回追加した games アプリ）
    #    http://127.0.0.1:8000/games/
    path("games/", include("apps.games.urls")),
]
