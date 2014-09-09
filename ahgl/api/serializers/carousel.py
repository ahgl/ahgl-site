from ahgl.api.models import CarouselItem
from rest_framework import serializers


class CarouselItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CarouselItem
        fields = ('order', 'header_image_url', 'message',)

