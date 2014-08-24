from ahgl.api.models import Game
from rest_framework import viewsets
from ahgl.api.serializers import game

class GamesViewSet(viewsets.ModelViewSet):
	queryset = Game.objects.all()
	serializer_class = game.GameSerializer
