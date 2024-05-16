from django.urls import path
from resources import views

urlpatterns = [
    path('', views.index, name='home'),
    path('teams/<int:team_id>/', views.get_all_players_for_team, name='players'),
    path('teams/<int:team_id>/<int:player_id>/injuries/', views.injuries, name='injuries'),
    path('addinjury/', views.add_injury, name='add_injury'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
]
