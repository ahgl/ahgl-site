from rest_framework import serializers

from ahgl.tournaments.models import Match


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    home_team = serializers.SlugRelatedField(slug_field='name')
    away_team = serializers.SlugRelatedField(slug_field='name')
    tournament = serializers.SlugRelatedField(slug_field='name')

    background_image_url = serializers.SerializerMethodField('get_background_image_url')
    icon_image_url = serializers.SerializerMethodField('get_icon_image_url')

    match_url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Match
        fields = ('home_team', 'away_team', 'tournament', 'featured', 'background_image_url', 'icon_image_url', 'match_url')

    def get_icon_image_url(self, match):
        if match.tournament.game is None:
            return ""

        return match.tournament.game.icon_image_url

    def get_background_image_url(self, match):
        if match.tournament.game is None:
            return ""

        return match.tournament.game.background_match_image_url
