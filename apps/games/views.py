from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

# Models: apps.<app>.models のフルパスでインポート（プロジェクト構成に合わせる）
from apps.games.models import Game, Lineup, Inning
from apps.teams.models import Team
from apps.players.models import Player
from apps.scores.models import Pitch

# Forms (既存の GameForm を利用)
try:
    from .forms import GameForm
except Exception:
    GameForm = None  # 無ければ None にしておく（既に存在するはず）


# -------------------------
# 試合一覧 / 追加 / 編集 / 削除
# -------------------------
def game_list(request):
    """試合一覧を表示"""
    games = Game.objects.all().order_by("-game_datetime")
    return render(request, "games/game_list.html", {"games": games})


def game_add(request):
    """試合を追加"""
    if GameForm is None:
        return HttpResponseBadRequest("GameForm が見つかりません。forms.py を確認してください。")

    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("games:game_list")
    else:
        form = GameForm()
    return render(request, "games/game_form.html", {"form": form})


def game_edit(request, pk):
    """試合を編集"""
    if GameForm is None:
        return HttpResponseBadRequest("GameForm が見つかりません。forms.py を確認してください。")

    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect("games:game_list")
    else:
        form = GameForm(instance=game)
    return render(request, "games/game_form.html", {"form": form, "game": game})


def game_delete(request, pk):
    """試合を削除"""
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        game.delete()
        return redirect("games:game_list")
    return render(request, "games/game_delete.html", {"game": game})


# -------------------------
# スコア入力トップ
# -------------------------
def score_top(request, pk):
    """
    スコア入力トップ。
    - 先攻 / 後攻の Lineup 登録状態を判定してテンプレに渡す。
    - both_ready が True のときに投球開始ボタンを出す（テンプレ側で仮リンク／実リンクを制御）。
    """
    game = get_object_or_404(Game, pk=pk)

    first_team = game.first_batting
    second_team = game.second_batting

    # Lineup の存在チェック（exists としておく。厳密に 9 人揃いをチェックしたければ count==9 に変更）
    first_team_has_lineup = Lineup.objects.filter(game=game, team=first_team).exists()
    second_team_has_lineup = Lineup.objects.filter(game=game, team=second_team).exists()
    both_ready = first_team_has_lineup and second_team_has_lineup

    context = {
        "game": game,
        "first_team": first_team,
        "second_team": second_team,
        "first_team_has_lineup": first_team_has_lineup,
        "second_team_has_lineup": second_team_has_lineup,
        "both_ready": both_ready,
    }
    return render(request, "games/score_top.html", context)


# -------------------------
# メンバー表（lineup）入力（初回9枠 or 変更時も同じ画面で差分更新）
# URL 名: games:lineup_add
# path: /games/<game_id>/lineup/<team_id>/
# -------------------------
@require_http_methods(["GET", "POST"])
def lineup_add(request, game_id, team_id):
    """
    - GET: 既存の Lineup を読み出して 1..9 を初期表示（ない場合は空欄）
    - POST: 既存の Lineup を一旦削除して、1..9 の入力値で再作成
            → ただし Pitch が紐づいているため、先にこのチーム側の Pitch を削除する必要あり
    """
    game = get_object_or_404(Game, pk=game_id)
    team = get_object_or_404(Team, pk=team_id)

    # チーム所属選手（選択肢）
    players = Player.objects.filter(team=team).order_by("name")

    existing_lineups = Lineup.objects.filter(game=game, team=team).order_by("batting_order")

    # ----- GET -----
    if request.method == "GET":
        lineup_data = []
        for i in range(1, 10):
            try:
                entry = existing_lineups.get(batting_order=i)
                player_id = entry.player.id
                position = entry.position
            except Lineup.DoesNotExist:
                player_id = ""
                position = ""
            lineup_data.append({"order": i, "player": player_id, "position": position})

        return render(request, "games/lineup_add.html", {
            "game": game,
            "team": team,
            "players": players,
            "lineup_data": lineup_data,
            "position_choices": Player.POSITION_CHOICES,
        })

    # ----- POST（保存） -----

    # ① 先に Pitch を削除 (このチームが打者になっているものだけ)
    Pitch.objects.filter(game=game, hitter__team=team).delete()

    # ② lineup を削除
    Lineup.objects.filter(game=game, team=team).delete()

    # ③ lineup 再作成
    for i in range(1, 10):
        player_id = request.POST.get(f"player_{i}")
        position = request.POST.get(f"position_{i}")
        if player_id:
            Lineup.objects.create(
                game=game,
                team=team,
                batting_order=i,
                player_id=int(player_id),
                position=int(position) if position else None
            )

    return redirect("games:score_top", pk=game_id)


# -------------------------
# 投球開始（pitch_start）
#  - 設計書どおりに安全に実装できる最小構成で作る
#  - 打順/イニング/表裏の自動制御は別フェーズで追加する（現在は 1 回表 / 打順 1 番 固定）
# -------------------------
def _safe_create_pitch(pitch_model, kwargs):
    """
    Pitch モデルのフィールド名は過去の変更で揺れている可能性があるため、
    いくつかのキー候補セットを試して挿入するヘルパ。
    kwargs は共通情報 (game, inning, top_bottom, pitch_number, result, batter, pitcher) を含む。
    """
    # 試すフィールドパターン（プロジェクト内で想定されうるフィールド名）
    patterns = [
        # パターンA: (game, inning, top_bottom, pitch_number, result, batter, pitcher)
        ["game", "inning", "top_bottom", "pitch_number", "result", "batter", "pitcher"],
        # パターンB: (game, inning, top_bottom, pitch_number, pitch_result, batter, pitcher)
        ["game", "inning", "top_bottom", "pitch_number", "pitch_result", "batter", "pitcher"],
        # パターンC: (game, inning, top_bottom, pitch_number, result, hitter, pitcher)
        ["game", "inning", "top_bottom", "pitch_number", "result", "hitter", "pitcher"],
        # パターンD: (game, inning, top_bottom, pitch_number, pitch_result, hitter)
        ["game", "inning", "top_bottom", "pitch_number", "pitch_result", "hitter"],
        # パターンE: older style: (game, batting_order, hitter, pitch_result, atbat_result, pitch_number)
        ["game", "batting_order", "hitter", "pitch_result", "atbat_result", "pitch_number"],
    ]

    # try each pattern by building create_kwargs from provided kwargs
    for pattern in patterns:
        create_kwargs = {}
        ok = True
        for key in pattern:
            if key in kwargs:
                create_kwargs[key] = kwargs[key]
            else:
                ok = False
                break
        if not ok:
            continue
        try:
            return pitch_model.objects.create(**create_kwargs)
        except Exception:
            # 作成失敗したら次のパターンへ
            continue
    # 最終手段：try generic common fields if present
    try:
        return pitch_model.objects.create(**kwargs)
    except Exception:
        # それでもダメなら None を返して呼び出し元でログ出力する
        return None


@require_http_methods(["GET", "POST"])
def pitch_start(request, pk):
    game = get_object_or_404(Game, pk=pk)

    # --- 最新投球から inning/top_bottom/batting_order を推定 ---
    last_pitch = Pitch.objects.filter(game=game).order_by("-id").first()

    if last_pitch:
        inning = last_pitch.inning
        top_bottom = last_pitch.top_bottom
        next_batting = (last_pitch.batting_order or 0) + 1
        if next_batting > 9:
            next_batting = 1

        # --- 直近の投球で3アウトに到達している場合は次のイニングへ進める ---
        try:
            pitch_history_check = Pitch.objects.filter(game=game, inning=inning, top_bottom=top_bottom)
            outs_check = pitch_history_check.filter(pitch_result="out").count()
        except Exception:
            outs_check = 0

        if outs_check >= 3:
            # advance to next half-inning
            if top_bottom == "top":
                inning = inning
                top_bottom = "bottom"
            else:
                inning = inning + 1
                top_bottom = "top"
            # batting order continues: next batter is last_pitch.batting_order + 1
            next_batting = (last_pitch.batting_order or 0) + 1
            if next_batting > 9:
                next_batting = 1
    else:
        inning = 1
        top_bottom = "top"
        next_batting = 1

    # --- 今の回の投球履歴 ---
    pitch_history_current = Pitch.objects.filter(
        game=game, inning=inning, top_bottom=top_bottom
    ).order_by("id")

    # --- 攻撃/守備チーム（★Gameモデル準拠） ---
    if top_bottom == "top":
        offense_team = game.first_batting
        defense_team = game.second_batting
    else:
        offense_team = game.second_batting
        defense_team = game.first_batting

    # --- 打者（Lineupから取得） ---
    hitter_entry = Lineup.objects.filter(
        game=game, team=offense_team, batting_order=next_batting
    ).first()

    # --- 投手（守備側の position=1 が投手） ---
    pitcher_entry = Lineup.objects.filter(
        game=game, team=defense_team, position=1
    ).first()

    # ======================= POST（投球入力） ============================
    if request.method == "POST":
        result = request.POST.get("result")
        if not result:
            return HttpResponseBadRequest("投球結果が指定されていません。")

        # 試合全体の投球番号
        pitch_number = Pitch.objects.filter(game=game).count() + 1

        # 保存
        Pitch.objects.create(
            game=game,
            batting_order=next_batting,
            hitter=hitter_entry,
            pitch_result=result,
            atbat_result=None,
            pitch_number=pitch_number,
            inning=inning,
            top_bottom=top_bottom,
        )

        # --- आउट数を再計算 ---
        pitch_history_current = Pitch.objects.filter(
            game=game, inning=inning, top_bottom=top_bottom
        )
        outs = pitch_history_current.filter(pitch_result="out").count()

        # --- 3アウトならイニング遷移 ---
        if outs == 3:
            if top_bottom == "top":
                next_inning = inning
                next_top_bottom = "bottom"
                next_is_top = False
            else:
                next_inning = inning + 1
                next_top_bottom = "top"
                next_is_top = True

            Inning.objects.get_or_create(
                game=game,
                number=next_inning,
                top_bottom=next_top_bottom,
                defaults={"is_top": next_is_top}
            )

        return redirect("games:pitch_start", pk=pk)

    # ======================= GET（画面表示） ============================
    count_s = pitch_history_current.filter(pitch_result="strike").count()
    count_b = pitch_history_current.filter(pitch_result="ball").count()
    count_o = pitch_history_current.filter(pitch_result="out").count()

    inning_display = f"{inning}回{'表' if top_bottom == 'top' else '裏'}"

    context = {
        "game": game,
        "inning_display": inning_display,
        "offense_team": offense_team,
        "defense_team": defense_team,
        "batter": hitter_entry.player if hitter_entry else None,
        "batter_pos": hitter_entry.get_position_display() if hitter_entry else "",
        "pitcher": pitcher_entry.player if pitcher_entry else None,
        "count_s": count_s,
        "count_b": count_b,
        "count_o": count_o,
        "pitch_history": pitch_history_current,
    }
    return render(request, "games/pitch_start.html", context)
