from celery.task import task
from account.models import AccountDeletion

from django.contrib.auth.models import User
from notification import models as notification

@task(name="profiles.tasks.expunge_deleted", ignore_result=True)
def expunge_deleted():
    return AccountDeletion.expunge()

@task(ignore_result=True)
def notify_member_join_request(team, member, membership_id, captains):
    notification.send((User.objects.filter(pk__in=captains)),
                      "profiles_member_join_request",
                      {
                        'team': team,
                        'member': member,
                        'membership_id': membership_id})
