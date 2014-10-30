from celery.task import task
from account.models import AccountDeletion

from django.contrib.auth.models import User
from notification import models as notification
from announcements import signals


@task(name="profiles.tasks.expunge_deleted", ignore_result=True)
def expunge_deleted():
    return AccountDeletion.expunge()


@task(ignore_result=True)
def notify_member_join_request(team, member, membership_id, captains):
    notification.send((User.objects.filter(pk__in=captains)),
                      "profiles_member_join_request",
                      {'team': team,
                       'member': member,
                       'membership_id': membership_id})


@task(ignore_result=True)
def notify_team_registration(captain_id, contact_email):
    notification.send(User.objects.filter(pk=captain_id),
                      "registration_notice",
                      {'contact_email': contact_email})


@task(ignore_result=True)
def notify_announcement(title, description):
    notification.send(User.objects.all(),
                      "announcement",
                      {'description': description, 'title': title})


def wrapper_notify_announcement(**kwargs):
    announcement = kwargs['announcement']
    description = announcement.content
    title = announcement.title
    notify_announcement.delay(title, description)

# Connect django-announcement creation with django-notification send
signals.announcement_created.connect(wrapper_notify_announcement)
