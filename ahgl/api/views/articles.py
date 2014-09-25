from ahgl.tournaments.models import Article
from ahgl.tournaments.models import Tournament
from rest_framework import viewsets
from ahgl.api.serializers import article


class LatestNewsViewSet(viewsets.ModelViewSet):
    model = Article
    serializer_class = article.ArticleSerializer

    def get_queryset(self):
        limit = int(self.request.QUERY_PARAMS.get('limit', 2))
        tournament_slug = self.request.QUERY_PARAMS.get('tournament', None)

        if tournament_slug:
            tournament = Tournament.objects.filter(slug=tournament_slug, status='A')
            queryset = Article.objects.filter(tournaments=tournament, published=True).order_by('publish_date', 'creation_date')[:limit]

            for article in queryset:
                article.tournaments = tournament
                    
        else:
            queryset = Article.objects.filter(tournaments__status='A', published=True).distinct().order_by('publish_date', 'creation_date')[:limit]

        return queryset
