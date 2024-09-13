from django.urls import path

from resources import views

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team-list'),
    path('team/<slug:team_slug>/', views.TeamPlayerListView.as_view(), name='team-players'),
    path(
        'team/<slug:team_slug>/<slug:player_slug>/injuries/',
        views.PlayerInjuryListView.as_view(),
        name='player-injuries',
    ),
    path('contacts/', views.ContactPageView.as_view(), name='contacts'),
    path('login/', views.login, name='login'),
]
