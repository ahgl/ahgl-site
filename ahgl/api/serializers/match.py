from ahgl.tournaments.models import Match
from rest_framework import serializers

class MatchSerializer(serializers.HyperlinkedModelSerializer):
	home_team = serializers.SlugRelatedField(slug_field='name')
	away_team = serializers.SlugRelatedField(slug_field='name')
	tournament = serializers.SlugRelatedField(slug_field='name')

	class Meta:
		model = Match
		fields = ('home_team', 'away_team', 'tournament', 'featured')