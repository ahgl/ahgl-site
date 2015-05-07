from ahgl.api.models import Game
from rest_framework import serializers


class GameSerializer(serializers.HyperlinkedModelSerializer):
    tournament_slug = serializers.CharField(source='get_tournament_slug')
    channels = serializers.CharField(source='channel_name')

    class Meta:
        model = Game
        fields = ('name', 'header_image_url', 'live_stream_section_image_url',
                  'match_section_image_url', 'article_section_image_url',
                  'channels', 'tournament_slug', 'questions')
