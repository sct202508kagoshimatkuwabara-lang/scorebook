from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from .forms import GameForm

# 試合一覧
def game_list(request):
    games = Game.objects.all().order_by("-game_datetime")
    return render(request, "games/game_list.html", {"games": games})

# 試合追加
def game_add(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("games:game_list")
    else:
        form = GameForm()
    return render(request, "games/game_form.html", {"form": form})

# 試合編集
def game_edit(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect("games:game_list")
    else:
        form = GameForm(instance=game)
    return render(request, "games/game_form.html", {"form": form, "game": game})

# 試合削除
def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        game.delete()
        return redirect("games:game_list")
    return render(request, "games/game_delete.html", {"game": game})
