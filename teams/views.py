from django.shortcuts import render, get_object_or_404, redirect
from .models import Team
from .forms import TeamForm


# チーム一覧
def team_list(request):
    teams = Team.objects.all()
    return render(request, "teams/team_list.html", {"teams": teams})


# チーム作成
def team_create(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("team_list")
    else:
        form = TeamForm()
    return render(request, "teams/team_form.html", {"form": form})


# チーム編集
def team_edit(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect("team_list")
    else:
        form = TeamForm(instance=team)

    return render(request, "teams/team_form.html", {"form": form})


# チーム削除
def team_delete(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == "POST":
        team.delete()
        return redirect("team_list")

    return render(request, "teams/team_delete.html", {"team": team})

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = team.players.all()  # related_name="players" を利用

    return render(request, "teams/team_detail.html", {
        "team": team,
        "players": players,
    })
