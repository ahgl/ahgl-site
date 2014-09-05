from ahgl.tournaments.models import Article
from ahgl.api.models import Game
from rest_framework import serializers

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    tournaments = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    image_url = serializers.SerializerMethodField('get_image_url')
    page_url = serializers.CharField(source='get_absolute_url')

    class Meta:
        model = Article
        fields = ('title', 'summary', 'tournaments', 'image_url', 'page_url',)

    def get_image_url(self, article):
        image_url = None

        if hasattr(article, 'tournament'):
            game_queryset = Game.objects.filter(tournament=article.tournament)
                if game_queryset.exists():
                    image_url = game_queryset.get().image_url

        return image_url