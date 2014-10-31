from django.conf import settings


def account(request):
    ctx = {
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
    }
    return ctx