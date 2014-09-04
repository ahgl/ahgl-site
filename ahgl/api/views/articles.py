from ahgl.tournaments.models import Article
from rest_framework import viewsets
from ahgl.api.serializers import article

from itertools import chain

class LatestNewsViewSet(viewsets.ModelViewSet):
	model = Article
	serializer_class = article.ArticleSerializer

	def get_queryset(self):
		limit = self.request.QUERY_PARAMS.get('limit', 2)
		tournament = self.request.QUERY_PARAMS.get('tournament', None)

		if tournament:
			queryset = (Article.objects.filter(tournaments=tournament, published=True)
					.order_by('publish_date', 'creation_date'))[:limit]

			for article in queryset:
				article.tournament = tournament
				
		else:
			queryset = (Article.objects.filter(published=True)
					.order_by('publish_date', 'creation_date'))[:limit]

		return queryset