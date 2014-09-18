# A tag that includes the contents of a file in PROJECT_ROOT.
#
# For example, {% include_static_file "js/app/dist/main.html" %}
#
# The contents will be cached in memory if DEBUG is not set.

import os

from django import template
from django.conf import settings

register = template.Library()

cache = dict()

@register.simple_tag
def include_static_file(path):

    contents = cache.get(path)
    if contents is not None:
        return contents

    abspath = os.path.join(settings.PROJECT_ROOT, path)
    try:
        fh = open(abspath, 'r')
        contents = fh.read()
    except Exception as e:
        raise Exception("include_static_file tag could not read file at %s: %s" % (path, e))

    if not settings.DEBUG:
        cache[path] = contents

    return contents
