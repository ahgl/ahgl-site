# coding=utf8
from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError

from tournaments.models import TeamRoundMembership, Tournament
from profiles.models import Team


class Command(BaseCommand):
    args = '<tournament_slug>'
    help = 'Updates all stats for teams and team round memberships'

    def handle(self, *args, **options):
        try:
            self.tournament = Tournament.objects.get(slug=args[0])
        except Tournament.DoesNotExist:
            raise CommandError("Tournament {0} does not exist".format(args[0]))

        for team in Team.objects.filter(tournament=self.tournament):
            team.update_stats()
        for membership in TeamRoundMembership.objects.filter(tournamentround__tournament=self.tournament):
            membership.update_stats()
