from ahgl.tournaments.models import Article
from ahgl.api.models import Game
from rest_framework import serializers
from tournaments.models import ACTIVE_TOURNAMENT_STATUS


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    tournaments = serializers.SerializerMethodField('get_tournaments')
    icon_image_url = serializers.SerializerMethodField('get_icon_image_url')
    page_url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Article
        fields = ('title', 'summary', 'tournaments', 'icon_image_url', 'page_url', 'publish_date',)

    def get_icon_image_url(self, article):
        image_url = None

        game_queryset = Game.objects.filter(tournament__in=article.tournaments.all(), icon_image_url__isnull=False)
        if game_queryset.exists():
            image_url = game_queryset[0].icon_image_url

        return image_url

    def get_tournaments(self, article):
        tournaments = []
        for tournament in article.tournaments.all():
            if tournament.status in ACTIVE_TOURNAMENT_STATUS:
                tournaments.append(tournament.name)

        return tournaments
