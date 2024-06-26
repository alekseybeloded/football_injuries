from django.urls import path

from resources import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('team/<slug:team_slug>/', views.GetPlayersForTeam.as_view(), name='players'),
    path(
        'team/<slug:team_slug>/<slug:player_slug>/injuries/',
        views.GetInjuriesForPlayer.as_view(),
        name='injuries',
    ),
    path('contacts/', views.Contacts.as_view(), name='contacts'),
    path('login/', views.login, name='login'),
]
