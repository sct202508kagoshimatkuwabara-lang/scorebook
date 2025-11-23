from django.shortcuts import render, redirect
from .models import Game
from .forms import GameForm

# --------------------------
# ホーム画面
# --------------------------
def home(request):
    return render(request, "scores/home.html")

# --------------------------
# Game 一覧
# --------------------------
def game_list(request):
    games = Game.objects.all()
    return render(request, "scores/game_list.html", {"games": games})

# --------------------------
# Game 登録
# --------------------------
def game_create(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("game_list")
    else:
        form = GameForm()

    return render(request, "scores/game_form.html", {"form": form})
