from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

from apps.scores.models import Pitch
from apps.games.models import Game, Lineup
from apps.players.models import Player


class ScoreInputView(View):

    def get(self, request, game_id):

        game = Game.objects.get(id=game_id)

        # 全選手リスト（ランナー選択用）
        players = Player.objects.all().values("id", "name")
        players_json = json.dumps(list(players), cls=DjangoJSONEncoder)

        # 次の投球番号
        pitch_number = Pitch.objects.filter(game=game).count() + 1

        return render(request, "scores/form.html", {
            "game": game,
            "players_json": players_json,
            "pitch_number": pitch_number,
        })

    def post(self, request, game_id):

        game = Game.objects.get(id=game_id)

        inning = int(request.POST.get("inning"))
        top_bottom = request.POST.get("top_bottom")           # "top" or "bottom"
        pitch_number = int(request.POST.get("pitch_number"))
        pitch_result = request.POST.get("pitch_result")       # strike / ball / foul / inplay
        atbat_result = request.POST.get("atbat_result")       # "三振" / "アウト" / "" など

        # runner JSON
        runners_json = request.POST.get("runners_json")
        runners = json.loads(runners_json) if runners_json else []

        # ---- 打者の自動判定 ----
        # 最新の打席を確認し、次の打者を決める
        last_pitch = Pitch.objects.filter(game=game).order_by("-id").first()

        if last_pitch:
            next_order = last_pitch.batting_order + 1
        else:
            next_order = 1

        # 9番の次は1番へ
        if next_order > 9:
            next_order = 1

        lineup = Lineup.objects.filter(game=game, order_number=next_order).first()

        # ---- Pitch 保存 ----
        pitch = Pitch()
        pitch.game = game
        pitch.inning = inning
        pitch.top_bottom = top_bottom
        pitch.pitch_number = pitch_number
        pitch.pitch_result = pitch_result
        pitch.atbat_result = atbat_result

        pitch.hitter = lineup
        pitch.batting_order = next_order

        # ---- ランナー保存 ----
        for r in runners:
            base = r["base"]       # 1 / 2 / 3
            player_id = r["id"]
            action = r["action"]   # stay / to2 / out / score など（scoreは無視）

            if action == "stay":
                if base == 1:
                    pitch.runner_1b_id = player_id
                elif base == 2:
                    pitch.runner_2b_id = player_id
                elif base == 3:
                    pitch.runner_3b_id = player_id

            # out / score は塁に残さないので処理しない

        pitch.save()

        return redirect("scores:input", game_id=game.id)


def get_lineup_api(request, game_id):
    """
    lineup を JSON で返す API
    """
    lineup = Lineup.objects.filter(game_id=game_id)\
        .values("id", "order_number", "player__name")
    return JsonResponse(list(lineup), safe=False)


def home(request):
    return render(request, "scores/home.html")
