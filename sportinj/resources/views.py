from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from resources.models import Team, Player, Injury


menu = [ 
    {'title': 'Добавить травму', 'url_name': 'add_injury'},
    {'title': 'Контакты', 'url_name': 'contacts'},
    {'title': 'Что-нибудь еще', 'url_name': 'login'},
]

def index(request):
    teams = Team.objects.all()
    data_of_teams = {
        'teams': teams,
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'resources/index.html', context=data_of_teams)

def get_all_players_for_team(request, team_slug):
    team = Team.objects.get(slug=team_slug)
    players = Player.objects.filter(team_id=team.id)
    data_of_players = {
        'players': players,
        'team': team,
        'menu': menu,
        'title': 'Страница с игроками'
    }
    return render(request, 'resources/player.html', context=data_of_players)

def injury(request, team_slug, player_slug):
    player = Player.objects.get(slug=player_slug)
    injury = Injury.objects.get(player_id=player.id)
    data_of_injuries = {
        'injury': injury,
        'menu': menu,
        'title': 'Страница с травмами'
    }
    return render(request, 'resources/injury.html', context=data_of_injuries)

def add_injury(request):
    return HttpResponse('Добавление травмы')

def contacts(request):
    return HttpResponse('Контакты')

def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

