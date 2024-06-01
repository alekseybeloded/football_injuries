from django.urls import path
from resources import views

urlpatterns = [
    path('', views.index, name='home'),
    path('team/<slug:team_slug>/', views.get_all_players_for_team, name='players'),
    path('team/<slug:team_slug>/<slug:player_slug>/injuries/', views.injury, name='injuries'),
    path('addplayer/', views.add_player, name='add_player'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
]
