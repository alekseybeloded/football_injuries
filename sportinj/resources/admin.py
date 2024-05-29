from django.contrib import admin
from resources.models import Team, Player, Injury


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('id', 'name', 'time_create')
    list_display_links=('id', 'name')
    ordering = ['time_create']
    list_per_page = 20
    search_fields = ['name']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    filter_horizontal = ['injuries']
    list_display = ('id', 'name', 'team', 'get_injuries_for_player', 'time_create')
    list_display_links = ('id', 'name')
    ordering = ['time_create']
    list_per_page = 20
    search_fields = ['name']
    list_filter = ['injuries', 'team']

    @admin.display(description='injuries')
    def get_injuries_for_player(self, player):
        return list(player.injuries.all())


@admin.register(Injury)
class InjuryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_all_players_with_specific_injury', 'description', 'time_create')
    list_display_links = ('id', 'name')
    ordering = ['time_create']
    list_editable = ('description', )
    list_per_page = 20
    search_fields = ['name']
    list_filter = ['name']

    @admin.display(description='players')
    def get_all_players_with_specific_injury(self, injury):
        return list(injury.players.all())