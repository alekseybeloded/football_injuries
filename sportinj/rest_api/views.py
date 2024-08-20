from resources.models import Injury, Player, Team
from rest_framework import viewsets

from rest_api.serializers import InjurySerializer, PlayerSerializer, TeamSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class InjuryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Injury.objects.all()
    serializer_class = InjurySerializer
