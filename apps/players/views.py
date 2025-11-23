from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Player
from .forms import PlayerForm


# 選手一覧
def player_list(request):
    players = Player.objects.select_related("team").all()
    return render(request, "players/player_list.html", {"players": players})


# 選手登録
def player_create(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("player_list")
    else:
        form = PlayerForm()
    return render(request, "players/player_form.html", {"form": form, "title": "選手登録"})


# 選手編集
def player_edit(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect("player_list")
    else:
        form = PlayerForm(instance=player)

    return render(request, "players/player_form.html", {"form": form, "title": "選手編集"})


# 選手削除
def player_delete(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == "POST":
        player.delete()
        return redirect("player_list")

    return render(request, "players/player_delete.html", {"player": player})
