from ahgl.api.models import CarouselItem
from rest_framework import viewsets
from ahgl.api.serializers import carousel

class CarouselItemViewSet(viewsets.ModelViewSet):
	queryset = CarouselItem.objects.all()
	serializer_class = carousel.CarouselItemSerializer
