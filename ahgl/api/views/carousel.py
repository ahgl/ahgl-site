from ahgl.api.models import CarouselItem
from ahgl.tournaments.models import Tournament
from rest_framework import viewsets
from ahgl.api.serializers import carousel
from django.db.models import Q

class CarouselItemViewSet(viewsets.ModelViewSet):
    queryset = CarouselItem.objects.all()
    serializer_class = carousel.CarouselItemSerializer

    def get_queryset(self):
        tournament_slug = self.request.QUERY_PARAMS.get('tournament', None)

        if tournament_slug:
            tournament = Tournament.objects.filter(Q(status='A') | Q(status='S'), slug=tournament_slug)
            queryset = CarouselItem.objects.filter(tournaments=tournament)

            for item in queryset:
                item.tournaments = tournament
                    
        else:
            queryset = CarouselItem.objects.filter(Q(tournaments__status='A') | Q(tournaments__status='S'))

        return queryset
