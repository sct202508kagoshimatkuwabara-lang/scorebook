from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # ホーム画面
    path("games/", views.game_list, name="game_list"),
    path("games/create/", views.game_create, name="game_create"),
]
