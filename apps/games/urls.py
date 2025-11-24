from django.urls import path
from . import views
from . import views_score_input

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

    # 投球開始（既存）
    path("<int:pk>/pitch/", views.pitch_start, name="pitch_start"),

    # ★ スコア入力画面（今回のメイン）
    path("<int:pk>/score_input/", views_score_input.score_input, name="score_input"),

    # ★ 投球保存（AJAX）
    path("<int:pk>/score_input/save/", views_score_input.save_pitch, name="score_input_save"),
]
