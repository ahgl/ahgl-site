from ahgl.api.models import Game
from rest_framework import serializers


class GameSerializer(serializers.HyperlinkedModelSerializer):
    game_slug = serializers.CharField(source='get_tournament_slug')
    channel_name = serializers.CharField(source='channel_name')

    class Meta:
        model = Game
        fields = ('name', 'header_image_url', 'live_stream_section_image_url',
                  'match_section_image_url', 'article_section_image_url',
                  'channel_name', 'game_slug')

