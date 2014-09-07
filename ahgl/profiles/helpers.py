from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from .models import TeamMemberInvite

def create_invite(team, email):
    try:
        invite = TeamMemberInvite(team=team, email=email)
        invite.save()
    except Exception as e:
        return False

    return True

def create_and_send_invite(team, email):
    errors = []

    try:
        validate_email(email)

    except Exception as e:
        errors.append(_("Invalid email %s") % email)

    # Create the invites
    is_saved = create_invite(team, email)
    if not is_saved:
        errors.append(_("Could not send an invite to %s") % email)

    if len(errors) > 0:
        return False, errors

    return True, None