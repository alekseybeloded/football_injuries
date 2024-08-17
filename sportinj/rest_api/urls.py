from django.urls import path

from rest_api import views

app_name = 'rest_api'

urlpatterns = [
    path('teams/', views.TeamApiView.as_view()),
]
