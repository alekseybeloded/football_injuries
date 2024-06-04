from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from resources.models import Team, Player
from resources.forms import AddPlayerForm
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


menu = [ 
    {'title': 'Добавить игрока', 'url_name': 'add_player'},
    {'title': 'Контакты', 'url_name': 'contacts'},
    {'title': 'Что-нибудь еще', 'url_name': 'login'},
]


class HomePage(ListView):
    model = Team
    template_name = 'resources/index.html'
    context_object_name = 'teams'
    extra_context = {
        'menu': menu,
        'title': 'Главная страница'
    }


class GetPlayersForTeam(ListView):
    template_name = 'resources/player.html'
    context_object_name = 'players'

    def get_queryset(self):
        self.team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        return Player.objects.filter(team__slug=self.kwargs['team_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['team'] = self.team
        context['title'] = 'Страница с игроками'
        return context


class GetInjuriesForPlayer(ListView):
    template_name = 'resources/injury.html'
    context_object_name = 'injuries'

    def get_queryset(self):
        player = get_object_or_404(Player, slug=self.kwargs['player_slug'])
        return player.injuries.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Страница с травмами'
        return context


class AddPlayer(FormView):
    form_class = AddPlayerForm
    template_name = 'resources/add_player.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление игрока',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

def contacts(request):
    return HttpResponse('Контакты')

def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

