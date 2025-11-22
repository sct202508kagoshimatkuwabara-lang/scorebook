from django.urls import path
from . import views

urlpatterns = [
    path("", views.player_list, name="player_list"),
    path("create/", views.player_create, name="player_create"),
    path("<int:player_id>/edit/", views.player_edit, name="player_edit"),
    path("<int:player_id>/delete/", views.player_delete, name="player_delete"),
]
