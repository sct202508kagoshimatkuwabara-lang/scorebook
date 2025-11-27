from django.urls import path
from . import views

app_name = "games"

urlpatterns = [
    path("", views.game_list, name="game_list"),
    path("<int:game_id>/", views.game_detail, name="game_detail"),
    path("<int:game_id>/score/", views.score_input, name="score_input"),
    path("<int:game_id>/add_batting/", views.add_batting, name="add_batting"),
    path("<int:game_id>/add_pitch/", views.add_pitch, name="add_pitch"),
]
