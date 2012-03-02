from django.contrib.auth.models import User
from django.db.models import Q
from celery.task import task
from notification import models as notification

from .models import TeamRoundMembership

@task(ignore_result=True)
def notify_match_creation(match, home_team, away_team, home_team_captain, away_team_captain):
    notification.send(User.objects.exclude(username='master') \
                                  .filter(Q(profile__teams__pk__in=(home_team, away_team))
                                          | Q(profile__pk__in=(home_team_captain, away_team_captain))
                                          ),
                      "tournaments_new_match",
                      {'match': unicode(match),
                       'home_team_captain': home_team_captain,
                       'away_team_captain': away_team_captain,
                       })
    
@task(ignore_result=True)
def update_round_stats(tournament_pk):
    for membership in TeamRoundMembership.objects.filter(tournamentround__tournament=tournament_pk):
        membership.update_stats()
