# From https://github.com/divio/django-cms/issues/491

from cms.plugins.snippet.models import Snippet
from cms.plugins.snippet.cms_plugins import SnippetPlugin
from django import template

register = template.Library()

@register.simple_tag
def show_snippet(name):
    try:
        return SnippetPlugin().render(
            {},
            type('obj', (object,), {'snippet' : Snippet.objects.get(name = name)}),
            None
        )['content']
    except Snippet.DoesNotExist:
        return "[No snippet named '%s']" % name
