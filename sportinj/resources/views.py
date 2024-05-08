from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponseNotFound


menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

def index(request):
    return render(request, 'resources/index.html', {'title': 'The main page'})

def get_all_teams(request):
    return render(request, 'resources/team.html', {'title': 'teams'})

def get_all_players_for_team(request, team_id):
    return render(request, 'resources/player.html', {'title': 'players'})


def players(request):
    return render(request, 'resources/player.html', {'title': 'players'})

def injuries(request, team_id, player_id):
    return render(request, 'resources/injury.html', {'title': 'injuries'})

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

