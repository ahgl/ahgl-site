from django.contrib.auth.models import User
from django.db.models import Q
from celery.task import task
from notification import models as notification

@task(ignore_result=True)
def notify_match_creation(match, home_team, away_team, home_team_captain, away_team_captain):
    master_user = User.objects.get(username='master')
    notification.send(User.objects.exclude(profile__user=master_user) \
                                  .filter(Q(profile__teams__pk__in=(home_team, away_team))
                                          | Q(profile__pk__in=(home_team_captain, away_team_captain))
                                          ),
                      "tournaments_new_match",
                      {'match': unicode(match),
                       'home_team_captain': home_team_captain,
                       'away_team_captain': away_team_captain,
                       })