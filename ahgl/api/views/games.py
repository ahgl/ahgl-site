from ahgl.api.models import Game
from rest_framework import viewsets
from ahgl.api.serializers import game
from django.db.models import Q

class GamesViewSet(viewsets.ModelViewSet):
     queryset = Game.objects.filter(Q(tournament__status='A') | Q(tournament__status='S'))
     serializer_class = game.GameSerializer
