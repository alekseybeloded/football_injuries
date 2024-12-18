from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, TemplateView

from resources.models import Injury, Player, Team
from resources.utils import ExtraContextMixin


class TeamListView(ExtraContextMixin, ListView):
    model = Team
    template_name = 'resources/index.html'
    context_object_name = 'teams'
    title_page = 'Homepage - Football injuries'
    paginate_by = 10

    def get_queryset(self):
        return Team.objects.all().values('slug', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class TeamPlayerListView(LoginRequiredMixin, ExtraContextMixin, ListView):
    template_name = 'resources/player.html'
    context_object_name = 'players'
    paginate_by = 10

    def get_queryset(self):
        return Player.objects.filter(team__slug=self.kwargs['team_slug']).values('name', 'slug')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=f'{self.kwargs["team_slug"].replace("-", " ").title()} players',
        )


class PlayerInjuryListView(ExtraContextMixin, ListView):
    template_name = 'resources/injury.html'
    context_object_name = 'injuries'
    title_page = 'Injuries'

    def get_queryset(self):
        return Injury.objects.filter(player__slug=self.kwargs['player_slug']).values('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=f'{self.kwargs["player_slug"].replace("-", " ").title()}"s injuries',
        )


@method_decorator(cache_page(timeout=None), name='get')
class ContactPageView(ExtraContextMixin, TemplateView):
    template_name = 'resources/contacts.html'
    title_page = 'Contacts'


@method_decorator(cache_page(timeout=None), name='get')
class Custom404View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'errors/404.html', status=404)
