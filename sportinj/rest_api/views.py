from resources.models import Team
from rest_framework import generics

from rest_api.serializers import TeamSerializer


class TeamApiView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
