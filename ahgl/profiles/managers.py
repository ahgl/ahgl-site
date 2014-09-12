from django.db import models

class TeamMembershipManager(models.Manager):
    def get_query_set(self):
        return super(TeamMembershipManager, self).get_query_set().filter(status='A')

    def awaitings(self):
        return super(TeamMembershipManager, self).get_query_set().filter(status='W')

    def all(self):
        return super(TeamMembershipManager, self).get_query_set()