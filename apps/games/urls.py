from django.urls import path
from . import views
from .views_score_input import score_input, add_pitch, delete_pitch

app_name = "games"

urlpatterns = [
    path("", views.game_list, name="game_list"),
    path("create/", views.game_add, name="game_add"),
    path("<int:pk>/edit/", views.game_edit, name="game_edit"),
    path("<int:pk>/delete/", views.game_delete, name="game_delete"),

    # スコア入力トップ
    path("<int:pk>/score/", views.score_top, name="score_top"),

    # メンバー表（先攻・後攻）
    path("<int:game_id>/lineup/<int:team_id>/", views.lineup_add, name="lineup_add"),

    # （旧）投球開始
    path("<int:pk>/pitch/", views.pitch_start, name="pitch_start"),

    # ======================
    # スコア入力（新）
    # ======================
    path("<int:game_id>/score-input/", score_input, name="score_input"),

    # ======================
    # API: 投球の追加・削除
    # ======================
    path("<int:game_id>/pitch/add/", add_pitch, name="add_pitch"),
    path("<int:game_id>/pitch/delete/", delete_pitch, name="delete_pitch"),
]
