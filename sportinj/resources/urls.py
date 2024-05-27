from django.urls import path
from resources import views

urlpatterns = [
    path('', views.index, name='home'),
    path('team/<slug:team_slug>/', views.get_all_players_for_team, name='players'),
    path('team/<slug:team_slug>/<slug:player_slug>/injury/', views.injury, name='injury'),
    path('addinjury/', views.add_injury, name='add_injury'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
]
