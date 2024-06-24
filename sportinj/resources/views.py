from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from resources.forms import AddPlayerForm
from resources.models import Player, Team
from resources.utils import MenuMixin


class HomePage(MenuMixin, ListView):
    model = Team
    template_name = 'resources/index.html'
    context_object_name = 'teams'
    title_page = 'Homepage - Football injuries'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class GetPlayersForTeam(LoginRequiredMixin, MenuMixin, ListView):
    template_name = 'resources/player.html'
    context_object_name = 'Players'
    paginate_by = 10

    def get_queryset(self):
        self.team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        return Player.objects.filter(team__slug=self.kwargs['team_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, team=self.team, title=f'{self.team} players')


class GetInjuriesForPlayer(MenuMixin, ListView):
    template_name = 'resources/injury.html'
    context_object_name = 'injuries'
    title_page = 'Injuries'
    paginate_by = 10

    def get_queryset(self):
        self.player = get_object_or_404(Player, slug=self.kwargs['player_slug'])
        return self.player.injuries.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f"{self.player}'s injuries")


class AddPlayer(LoginRequiredMixin, MenuMixin, FormView):
    form_class = AddPlayerForm
    template_name = 'resources/add_player.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление игрока'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def contacts(request):
    return HttpResponse('Контакты')


def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
