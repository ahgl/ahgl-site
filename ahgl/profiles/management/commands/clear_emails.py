# coding=utf8
from __future__ import print_function

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    args = ''
    help = 'Clears all emails from user profiles'

    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                user.email = ""
                user.save()
            except Exception:
                pass
