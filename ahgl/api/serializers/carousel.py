from ahgl.api.models import CarouselItem
from rest_framework import serializers


class CarouselItemSerializer(serializers.HyperlinkedModelSerializer):
    tournaments = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = CarouselItem
        fields = ('order', 'image_url', 'message', 'tournaments',)

