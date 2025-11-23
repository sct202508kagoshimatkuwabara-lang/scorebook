from django.urls import path
from . import views

urlpatterns = [
    path("", views.team_list, name="team_list"),
    path("<int:team_id>/", views.team_detail, name="team_detail"),  # ←追加！
    path("create/", views.team_create, name="team_create"),
    path("<int:team_id>/edit/", views.team_edit, name="team_edit"),
    path("<int:team_id>/delete/", views.team_delete, name="team_delete"),
]
