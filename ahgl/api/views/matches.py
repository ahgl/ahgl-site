from ahgl.tournaments.models import Match
from rest_framework import viewsets
from ahgl.api.serializers import match

from itertools import chain


class FeaturedMatchesViewSet(viewsets.ModelViewSet):
    model = Match
    serializer_class = match.MatchSerializer

    def get_queryset(self):
        limit = self.request.QUERY_PARAMS.get('limit', 4)
        game = self.request.QUERY_PARAMS.get('game', None)

        if game:
            queryset = (Match.objects.filter(tournament__game__slug=game, featured=True)
                        .order_by('publish_date', 'creation_date', 'tournament_round')
                        .select_related('home_team', 'away_team', 'tournament_round'))[:limit]
        else:
            queryset = (Match.objects.filter(tournament__status='A', featured=True)
                        .order_by('publish_date', 'creation_date', 'tournament_round')
                        .select_related('home_team', 'away_team', 'tournament_round'))[:limit]

            if queryset.count() < limit:
                additional_queryset = (Match.objects.filter(tournament__status='A', featured=False)
                                       .order_by('publish_date', 'creation_date', 'tournament_round')
                                       .select_related('home_team', 'away_team', 'tournament_round'))

                queryset = list(chain(queryset, additional_queryset))[:limit]

        return queryset
