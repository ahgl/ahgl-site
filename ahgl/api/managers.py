from django.db import models

from tournaments.models import ACTIVE_TOURNAMENT_STATUS


class GameManager(models.Manager):
    def active(self):
        return super(GameManager, self).get_query_set().filter(tournament__status__in=ACTIVE_TOURNAMENT_STATUS)


class CarouselItemManager(models.Manager):
    def active(self):
        return super(CarouselItemManager, self).get_query_set().filter(tournaments__status__in=ACTIVE_TOURNAMENT_STATUS)
