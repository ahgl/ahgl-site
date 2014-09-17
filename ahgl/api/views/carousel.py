from ahgl.api.models import CarouselItem
from rest_framework import viewsets
from ahgl.api.serializers import carousel

class CarouselItemViewSet(viewsets.ModelViewSet):
    queryset = CarouselItem.objects.all()
    serializer_class = carousel.CarouselItemSerializer

    def get_queryset(self):
        game = self.request.QUERY_PARAMS.get('game', None)

        if game:
            queryset = CarouselItem.objects.filter(tournaments__game__slug=game)

            for item in queryset:
                item.tournament = game
                    
        else:
            queryset = CarouselItem.objects.all()

        return queryset
