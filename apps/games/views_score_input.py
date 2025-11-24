from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from apps.games.models import Game
from apps.scores.models import Pitch
from apps.players.models import Player


# OUTになる打者結果
BATTER_OUT_MAP = {
    "strikeout": 1,
    "fly": 1,
    "groundout": 1,
    "lineout": 1,
    "double_play": 2,
}


def calc_current_state(game):
    """
    最新のPitchから現在の inning / top_bottom / outs を復元する。
    """
    last = Pitch.objects.filter(game=game).order_by("-id").first()

    # 試合開始前
    if not last:
        return 1, "top", 0

    inning = last.inning
    top_bottom = last.top_bottom

    # 現在の回のログを全取得してOUT数計算
    pitches = Pitch.objects.filter(
        game=game,
        inning=inning,
        top_bottom=top_bottom
    ).order_by("id")

    outs = 0
    for p in pitches:
        outs += BATTER_OUT_MAP.get(p.batter_result, 0)

    return inning, top_bottom, outs


@require_http_methods(["GET"])
def score_input(request, pk):
    game = get_object_or_404(Game, pk=pk)

    recent = Pitch.objects.filter(game=game).order_by("-id")[:10]

    # 先攻・後攻チームの選手一覧
    players = Player.objects.filter(
        team__in=[game.first_batting, game.second_batting]
    ).order_by("team", "name")

    return render(request, "games/score_input/index.html", {
        "game": game,
        "recent_pitches": list(recent[::-1]),
        "players": players,   # ←追加
    })


@csrf_exempt
@require_http_methods(["POST"])
def save_pitch(request, pk):
    """ 投球1件を保存して、最新10件を返す """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except:
        return HttpResponseBadRequest("invalid json")

    game = get_object_or_404(Game, pk=pk)

    batter_id = payload.get("batter_id")
    pitcher_id = payload.get("pitcher_id")
    pitch_result = payload.get("pitch_result")
    batter_result = payload.get("batter_result")
    runner_action = payload.get("runner_action", "")

    if not (batter_id and pitcher_id and pitch_result and batter_result):
        return HttpResponseBadRequest("missing required")

    # 現在の状態を取得
    inning, top_bottom, outs = calc_current_state(game)

    # 今回の1球のアウト数
    increment = BATTER_OUT_MAP.get(batter_result, 0)
    outs += increment

    # 3アウトでイニング切り替え
    if outs >= 3:
        outs = 0
        if top_bottom == "top":
            top_bottom = "bottom"
        else:
            top_bottom = "top"
            inning += 1

    # 保存
    Pitch.objects.create(
        game=game,
        inning=inning,
        top_bottom=top_bottom,
        batter_id=batter_id,
        pitcher_id=pitcher_id,
        pitch_result=pitch_result,
        batter_result=batter_result,
        runner_action=runner_action,
    )

    # 最新10件返却
    recent = Pitch.objects.filter(game=game).order_by("-id")[:10]
    data = [{
        "id": p.id,
        "inning": p.inning,
        "top_bottom": p.top_bottom,
        "batter_id": p.batter_id_id,
        "pitcher_id": p.pitcher_id_id,
        "batter_result": p.batter_result,
    } for p in list(recent[::-1])]

    return JsonResponse({"ok": True, "pitches": data})
