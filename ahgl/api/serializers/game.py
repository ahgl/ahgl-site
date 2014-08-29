from ahgl.api.models import Game
from rest_framework import serializers

class GameSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Game
		fields = ('name','image_url','live_stream_image_url','channel_name',)
