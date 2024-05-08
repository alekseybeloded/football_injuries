from django.urls import path
from resources import views

urlpatterns = [
    path('', views.index, name='home'),
    path('teams/', views.get_all_teams, name='teams'),
    path('teams/<int:team_id>/', views.get_all_players_for_team, name='players'),
    path('teams/<int:team_id>/<int:player_id>/injuries/', views.injuries, name='injuries'),
]
