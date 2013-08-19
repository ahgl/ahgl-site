# This really should be a patch to https://github.com/pinax/django-forms-bootstrap
# but I'm short on time.

from django import template
from django.template import Context
from django.template.loader import get_template

register = template.Library()

@register.filter
def as_bootstrap_field(field):
    template = get_template("bootstrap/field.html")
    c = Context({"field": field})
    return template.render(c)
