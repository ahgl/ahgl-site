from ahgl.api.models import CarouselItem
from rest_framework import serializers

from tournaments.models import ACTIVE_TOURNAMENT_STATUS


class CarouselItemSerializer(serializers.HyperlinkedModelSerializer):
    tournaments = serializers.SerializerMethodField('get_tournaments')

    class Meta:
        model = CarouselItem
        fields = ('order', 'image_url', 'message', 'tournaments',)

    def get_tournaments(self, carousel):
        tournaments = []
        for tournament in carousel.tournaments.all():
            if tournament.status in ACTIVE_TOURNAMENT_STATUS:
                tournaments.append(tournament.name)

        return tournaments

