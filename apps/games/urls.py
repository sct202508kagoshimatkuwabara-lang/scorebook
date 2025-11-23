from django.urls import path
from . import views

app_name = "games"   # ←絶対に必要！！！

urlpatterns = [
    path("", views.game_list, name="game_list"),
    path("create/", views.game_add, name="game_add"),
    path("<int:pk>/edit/", views.game_edit, name="game_edit"),
    path("<int:pk>/delete/", views.game_delete, name="game_delete"),
]
