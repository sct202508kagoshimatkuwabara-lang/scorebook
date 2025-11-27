from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from apps.players.models import Player
from apps.teams.models import Team
from apps.games.models import Game, Score
from apps.scores.models import Pitch


def game_list(request):
    games = Game.objects.all().order_by("-game_datetime")
    return render(request, "games/game_list.html", {"games": games})


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    team_home_players = Player.objects.filter(team=game.first_batting)
    team_away_players = Player.objects.filter(team=game.second_batting)

    return render(
        request,
        "games/game_detail.html",
        {
            "game": game,
            "team_home_players": team_home_players,
            "team_away_players": team_away_players,
        },
    )


def score_input(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    batters = Score.objects.filter(game=game).order_by("order")
    pitches = Pitch.objects.filter(score__game=game).order_by("pitch_number")

    if request.method == "POST":
        # Save score data
        for batter in batters:
            batter.result = request.POST.get(f"result_{batter.id}", batter.result)
            batter.save()

        # Save pitch data
        for pitch in pitches:
            pitch.pitch_type = request.POST.get(f"pitch_type_{pitch.id}", pitch.pitch_type)
            pitch.speed = request.POST.get(f"speed_{pitch.id}", pitch.speed)
            pitch.result_type = request.POST.get(f"pitch_result_{pitch.id}", pitch.result_type)
            pitch.save()

        return redirect(reverse("games:score_input", args=[game_id]))

    return render(
        request,
        "games/score_input/score_input.html",
        {
            "game": game,
            "batters": batters,
            "pitches": pitches,
        },
    )


def add_pitch(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    # Create a new pitch entry
    new_pitch = Pitch.objects.create(
        score=None,  # You can update this logic to properly link the pitch to a score
        pitch_number=1,  # Example value, adjust as needed
        pitch_type="",
        speed=0,
        result_type="",
    )

    return redirect(reverse("games:score_input", args=[game_id]))


def add_batting(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    order = Score.objects.filter(game=game).count() + 1

    # Create a new batting entry
    new_batting = Score.objects.create(
        game=game,
        batter=None,  # Adjust to add a valid batter
        pitcher=None,  # Adjust to add a valid pitcher
        inning=1,  # Example value, adjust as needed
        result="",
        order=order,
    )

    return redirect(reverse("games:score_input", args=[game_id]))
