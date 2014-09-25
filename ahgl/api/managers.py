from django.db import models
from django.db.models import Q

class GameManager(models.Manager):
    def active(self):
        return super(GameManager, self).get_query_set().filter(Q(tournament__status='A') | Q(tournament__status='S'))

class CarouselItemManager(models.Manager):
    def active(self):
        return super(CarouselItemManager, self).get_query_set().filter(Q(tournaments__status='A') | Q(tournaments__status='S'))
