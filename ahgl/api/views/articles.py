from ahgl.tournaments.models import Article
from rest_framework import viewsets
from ahgl.api.serializers import article


class LatestNewsViewSet(viewsets.ModelViewSet):
    model = Article
    serializer_class = article.ArticleSerializer

    def get_queryset(self):
        limit = self.request.QUERY_PARAMS.get('limit', 2)
        game = self.request.QUERY_PARAMS.get('game', None)

        if game:
            queryset = Article.objects.filter(tournaments__game__slug=game, published=True).order_by('publish_date', 'creation_date')[:limit]

            for article in queryset:
                article.tournament = game
                    
        else:
            queryset = Article.objects.filter(published=True).order_by('publish_date', 'creation_date')[:limit]

        return queryset
