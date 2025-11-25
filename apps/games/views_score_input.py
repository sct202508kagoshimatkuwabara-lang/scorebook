# apps/games/views_score_input.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import F
import json

from apps.games.models import Game, Lineup
from apps.scores.models import Pitch


# ---------------------------------------------------------
# スコア入力画面（メイン）
# ---------------------------------------------------------
def score_input(request, pk):
    game = get_object_or_404(Game, pk=pk)

    # lineup 取得（先攻・後攻）
    top_team = game.first_batting
    bottom_team = game.second_batting

    top_lineups = list(game.lineups.filter(team=top_team).order_by("batting_order"))
    bottom_lineups = list(game.lineups.filter(team=bottom_team).order_by("batting_order"))

    # バッティング = 1〜9番の打順
    top_batting = [
        {"id": lu.player.id, "name": lu.player.name, "order": lu.batting_order}
        for lu in top_lineups
    ]
    bottom_batting = [
        {"id": lu.player.id, "name": lu.player.name, "order": lu.batting_order}
        for lu in bottom_lineups
    ]

    # 投手（position=1：投手）
    top_pitchers = [
        {"id": lu.player.id, "name": lu.player.name, "position": "P"}
        for lu in top_lineups if lu.position == 1
    ]
    bottom_pitchers = [
        {"id": lu.player.id, "name": lu.player.name, "position": "P"}
        for lu in bottom_lineups if lu.position == 1
    ]

    # lineup を JS に渡す形式に変換
    lineup_json = {
        "top": {
            "batting": top_batting,
            "pitching": top_pitchers,
        },
        "bottom": {
            "batting": bottom_batting,
            "pitching": bottom_pitchers,
        }
    }

    # 最新10件の投球
    recent = Pitch.objects.filter(game=game).order_by("-id")[:10]
    context = {
        "game": game,
        "lineup_json": json.dumps(lineup_json, ensure_ascii=False),
        "recent_pitches": recent,

        # ★ これが今回必要だった！
        "game_date": game.game_datetime,
        "team_home": game.first_batting,
        "team_away": game.second_batting,
    }
    return render(request, "games/score_input/index.html", context)


# ---------------------------------------------------------
# 投球保存（AJAX）
# ---------------------------------------------------------
@require_POST
def save_pitch(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

    data = json.loads(request.body)

    # --- 受け取る値 ---
    inning = data.get("inning")
    top_bottom = data.get("top_bottom")       # 'top' or 'bottom'
    pitch_number = data.get("pitch_number")   # 1球目、2球目…
    batting_order = data.get("batting_order") # 1〜9
    hitter_id = data.get("hitter_id")         # Lineup.id
    pitch_result = data.get("pitch_result")   # ball/strike/foul/inplay/hit/out
    atbat_result = data.get("atbat_result")   # 任意

    # hitter（Lineup）
    hitter = None
    if hitter_id:
        hitter = Lineup.objects.filter(id=hitter_id).first()

    # --- Pitchレコード作成 ---
    pitch = Pitch.objects.create(
        game=game,
        inning=inning,
        top_bottom=top_bottom,
        pitch_number=pitch_number,
        batting_order=batting_order,
        hitter=hitter,
        pitch_result=pitch_result,
        atbat_result=atbat_result,
    )

    return JsonResponse({
        "status": "ok",
        "pitch_id": pitch.id,
        "created_at": pitch.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    })


# ---------------------------------------------------------
# （未実装）最後の投球を削除
# ---------------------------------------------------------
def delete_last_pitch(request, pk):
    return JsonResponse({"error": "not implemented yet"})
