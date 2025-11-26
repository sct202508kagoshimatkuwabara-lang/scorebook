import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.games.models import Game, Lineup
from apps.players.models import Player
from apps.scores.models import Pitch


# ------------------------------------------------------------
# スコア入力画面
# ------------------------------------------------------------
def score_input(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # lineup_json（DB保存 dict）→ JS用に JSON 化
    lineup_json_safe = json.dumps(game.lineup_json, ensure_ascii=False)

    # 最新10件
    recent_pitches = Pitch.objects.filter(game_id=game.id).order_by("-id")[:10]
    recent_pitches = reversed(list(recent_pitches))

    recent_list = []
    for p in recent_pitches:
        recent_list.append({
            "id": p.id,
            "inning": p.inning,
            "top_bottom": p.top_bottom,
            "pitch_number": p.pitch_number,
            "batting_order": p.batting_order,
            "batter_id": p.hitter.player.id,
            "batter_name": p.hitter.player.name,
            "pitcher_id": p.pitcher.player.id,
            "pitcher_name": p.pitcher.player.name,
            "pitch_result": p.pitch_result,
            "atbat_result": p.atbat_result,
            "runner_action": getattr(p, "runner_action", ""),
        })

    recent_pitches_json = json.dumps(recent_list, ensure_ascii=False)

    return render(request, "games/score_input/score_input.html", {
        "game": game,
        "lineup_json": lineup_json_safe,
        "recent_pitches_json": recent_pitches_json,
        "recent_pitches": recent_list,
    })


# ------------------------------------------------------------
# Pitch 追加（AJAX）
# ------------------------------------------------------------
@require_POST
def add_pitch(request, game_id):
    try:
        body = json.loads(request.body)
    except:
        return JsonResponse({"error": "JSON decode error"}, status=400)

    game = get_object_or_404(Game, id=game_id)

    inning = body.get("inning")
    top_bottom = body.get("top_bottom")
    pitch_number = body.get("pitch_number")
    batting_order = body.get("batting_order")
    batter_id = body.get("batter_id")
    pitcher_id = body.get("pitcher_id")
    pitch_result = body.get("pitch_result")
    atbat_result = body.get("atbat_result")
    runner_action = body.get("runner_action", "")

    # Player → Lineup
    batter_player = Player.objects.get(id=batter_id)
    pitcher_player = Player.objects.get(id=pitcher_id)

    batter_lineup = Lineup.objects.get(game=game, player=batter_player)
    pitcher_lineup = Lineup.objects.get(game=game, player=pitcher_player)

    pitch = Pitch.objects.create(
        game=game,
        inning=inning,
        top_bottom=top_bottom,
        pitch_number=pitch_number,
        batting_order=batting_order,
        hitter=batter_lineup,
        pitcher=pitcher_lineup,  # ← 修正（確定）
        pitch_result=pitch_result,
        atbat_result=atbat_result,
        runner_action=runner_action or "",
    )

    return JsonResponse({
        "status": "ok",
        "pitch_id": pitch.id,
    })


# ------------------------------------------------------------
# Pitch 削除（AJAX）
# ------------------------------------------------------------
@require_POST
def delete_pitch(request, game_id):
    try:
        body = json.loads(request.body)
        pitch_id = body.get("pitch_id")
    except:
        return JsonResponse({"error": "JSON decode error"}, status=400)

    pitch = get_object_or_404(Pitch, id=pitch_id)
    pitch.delete()

    return JsonResponse({"status": "ok"})
