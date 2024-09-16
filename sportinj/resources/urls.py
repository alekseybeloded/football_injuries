from django.urls import path

from resources import views

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team-list'),
    path('teams/<slug:team_slug>/', views.TeamPlayerListView.as_view(), name='team-players'),
    path(
        'players/<slug:player_slug>/',
        views.PlayerInjuryListView.as_view(),
        name='player-injuries',
    ),
    path('contacts/', views.ContactPageView.as_view(), name='contacts'),
]
