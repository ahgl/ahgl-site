from ahgl.api.models import Game
from rest_framework import viewsets
from ahgl.api.serializers import header

class HeaderViewSet(viewsets.ModelViewSet):
	queryset = Game.objects.all()
	serializer_class = header.HeaderSerializer
