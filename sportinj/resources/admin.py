from django.contrib import admin

from resources.models import Injury, Player, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'time_create')
    list_display_links = ('id', 'name')
    ordering = ['time_create']
    list_per_page = 20
    search_fields = ['name']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'team', 'time_create')
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
    list_display = (
        'id',
        'name',
        'description',
        'time_create',
    )
    list_display_links = ('id', 'name')
    ordering = ['time_create']
    list_editable = ('description',)
    list_per_page = 20
    search_fields = ['name']
    list_filter = ['name']
