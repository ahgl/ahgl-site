from ahgl.tournaments.models import Match
from rest_framework import viewsets
from ahgl.api.serializers import match
from django.db.models import Q

from itertools import chain


class FeaturedMatchesViewSet(viewsets.ModelViewSet):
    model = Match
    serializer_class = match.MatchSerializer

    def get_queryset(self):
        limit = int(self.request.QUERY_PARAMS.get('limit', 4))
        tournament = self.request.QUERY_PARAMS.get('tournament', None)

        if tournament:
            queryset = (Match.objects.active().filter(tournament__slug=tournament, featured=True)
                        .order_by('publish_date', 'creation_date', 'tournament_round')
                        .select_related('home_team', 'away_team', 'tournament_round'))[:limit]
        else:
            queryset = (Match.objects.active().filter(featured=True)
                        .order_by('publish_date', 'creation_date', 'tournament_round')
                        .select_related('home_team', 'away_team', 'tournament_round'))[:limit]

            if queryset.count() < limit:
                additional_queryset = (Match.objects.active().filter(featured=False)
                                       .order_by('publish_date', 'creation_date', 'tournament_round')
                                       .select_related('home_team', 'away_team', 'tournament_round'))

                queryset = list(chain(queryset, additional_queryset))[:limit]

        return queryset
