from ahgl.tournaments.models import Article
from ahgl.api.models import Game
from rest_framework import serializers


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    tournaments = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
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
