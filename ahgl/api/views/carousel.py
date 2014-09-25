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
            tournament = Tournament.objects.filter(slug=tournament_slug)
            queryset = CarouselItem.objects.active().filter(tournaments=tournament)

            for item in queryset:
                item.tournaments = tournament
                    
        else:
            queryset = CarouselItem.objects.active()

        return queryset
