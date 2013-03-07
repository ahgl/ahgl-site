from uuid import uuid4
import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from social_auth.backends.pipeline import USERNAME, USERNAME_MAX_LENGTH
from idios.models import create_profile

from ..models import Profile

logger = logging.getLogger(__name__)

def get_username(details, response, user=None, *args, **kwargs):
    """Return an username for new user. Return current user username
    if user was given.
    """
    if user:
        return {'username': user.username}

    if details.get(USERNAME):
        username = details[USERNAME]
    elif response.get('name'):
        username = slugify(response['name'])
    else:
        username = uuid4().get_hex()

    uuid_lenght = getattr(settings, 'SOCIAL_AUTH_UUID_LENGTH', 16)
    username_fixer = getattr(settings, 'SOCIAL_AUTH_USERNAME_FIXER',
                             lambda u: u)

    short_username = username[:USERNAME_MAX_LENGTH - uuid_lenght]
    final_username = None

    while True:
        final_username = username_fixer(username)[:USERNAME_MAX_LENGTH]

        try:
            User.objects.get(username=final_username)
        except User.DoesNotExist:
            break
        else:
            # User with same username already exists, generate a unique
            # username for current user using username as base but adding
            # a unique hash at the end. Original username is cut to avoid
            # the field max_length.
            username = short_username + uuid4().get_hex()[:uuid_lenght]
    return {'username': final_username}


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not username:
        return None

    email = details.get('email')
    name = response.get('name')
    if name:
        # if they already have a profile created for them, use that profile
        try:
            master_user = User.objects.get(username='master')
            profile = Profile.objects.get(name=name, user=master_user)
        except Profile.DoesNotExist:
            pass
        else:
            logger.info('Using existing profile for social-auth with name {0}'.format(profile.name))
            post_save.disconnect(create_profile, sender=User)
            user = User.objects.create_user(username=username, email=email)
            post_save.connect(create_profile, sender=User)
            # in case we already associated by email to an existing account and profile...
            if not Profile.objects.filter(user=user).count():
                profile.user = user
                profile.save()
        
    if not user:
        user = User.objects.create_user(username=username, email=email)
    return {
        'user': user,
        'is_new': True
    }
