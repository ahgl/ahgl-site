from django.db import models
from django.db.models import Q

class ArticleManager(models.Manager):
    def active(self):
        return super(ArticleManager, self).get_query_set().filter(Q(tournaments__status='A') | Q(tournaments__status='S'))

class MatchManager(models.Manager):
    def active(self):
        return super(MatchManager, self).get_query_set().filter(Q(tournament__status='A') | Q(tournament__status='S'))