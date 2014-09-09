from ahgl.api.models import Game
from rest_framework import serializers


class HeaderSerializer(serializers.HyperlinkedModelSerializer):
    game_slug = serializers.CharField(source='tournament.slug', read_only=True)

    class Meta:
        model = Game
        fields = ('header_image_url', 'game_slug')
