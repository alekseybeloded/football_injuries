from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponse
from resources.models import Team, Player
from resources.forms import AddPlayerForm


menu = [ 
    {'title': 'Добавить игрока', 'url_name': 'add_player'},
    {'title': 'Контакты', 'url_name': 'contacts'},
    {'title': 'Что-нибудь еще', 'url_name': 'login'},
]

def index(request):
    teams = Team.objects.all()
    teams_context_data = {
        'teams': teams,
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'resources/index.html', context=teams_context_data)

def get_all_players_for_team(request, team_slug):
    team = Team.objects.get(slug=team_slug)
    players = Player.objects.filter(team_id=team.id)
    players_context_data = {
        'players': players,
        'team': team,
        'menu': menu,
        'title': 'Страница с игроками'
    }
    return render(request, 'resources/player.html', context=players_context_data)

def injury(request, team_slug, player_slug):
    player = Player.objects.get(slug=player_slug)
    injuries = player.injuries.all()
    injuries_context_data = {
        'injuries': injuries,
        'menu': menu,
        'title': 'Страница с травмами'
    }
    return render(request, 'resources/injury.html', context=injuries_context_data)

def add_player(request):
    if request.method == 'POST':
        form = AddPlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form =AddPlayerForm()

    add_player_context_data = {
        'menu': menu,
        'form': form
    }
    return render(request, 'resources/add_player.html', context=add_player_context_data)

def contacts(request):
    return HttpResponse('Контакты')

def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

