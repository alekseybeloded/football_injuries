from resources.models import Injury, Player, Team
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'description')


class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Player
        fields = ('name', 'description', 'team')


class InjurySerializer(serializers.ModelSerializer):
    class Meta:
        model = Injury
        fields = ('name', 'description')
