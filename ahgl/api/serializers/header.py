from ahgl.api.models import Game
from rest_framework import serializers

class HeaderSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Game
		fields = ('image_url',)