from ahgl.api.models import Game
from rest_framework import serializers


class GameSerializer(serializers.HyperlinkedModelSerializer):
    game_slug = serializers.CharField(source='tournament.slug', read_only=True)

    class Meta:
        model = Game
        fields = ('name', 'image_url', 'live_stream_image_url', 'channel_name', 'game_slug')


