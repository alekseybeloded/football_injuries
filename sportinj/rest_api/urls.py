from django.urls import include, path
from rest_framework import routers

from rest_api import views

app_name = 'rest_api'

team_router = routers.SimpleRouter()
team_router.register(r'teams', views.TeamViewSet)

player_router = routers.SimpleRouter()
player_router.register(r'players', views.PlayerViewSet)

injury_router = routers.SimpleRouter()
injury_router.register(r'injuries', views.InjuryViewSet)

urlpatterns = [
    path('', include(team_router.urls)),
    path('', include(player_router.urls)),
    path('', include(injury_router.urls)),
]
