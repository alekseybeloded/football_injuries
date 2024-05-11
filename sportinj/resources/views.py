from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponseNotFound
from resources.models import Team, Player, Injury


menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

def index(request):
    teams = Team.objects.all()
    return render(request, 'resources/index.html', {'teams': teams})

def get_all_teams(request):
    return render(request, 'resources/team.html', {'title': 'teams'})

def get_all_players_for_team(request, team_id):
    players = Player.objects.filter(team_id=team_id)
    return render(request, 'resources/player.html', {'players': players})

def injuries(request, team_id, player_id):
    injuries = Injury.objects.filter(player_id=player_id)
    return render(request, 'resources/injury.html', {'injuries': injuries})

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

