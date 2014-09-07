from ahgl.tournaments.models import Match
from rest_framework import serializers


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    home_team = serializers.SlugRelatedField(slug_field='name')
    away_team = serializers.SlugRelatedField(slug_field='name')
    tournament = serializers.SlugRelatedField(slug_field='name')
    background_image_url = serializers.CharField(source='get_background_image_url')
    match_url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Match
        fields = ('home_team', 'away_team', 'tournament', 'featured', 'background_image_url', 'match_url')
