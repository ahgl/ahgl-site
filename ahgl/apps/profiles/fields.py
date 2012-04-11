import bleach

from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe

from tinymce.widgets import TinyMCE

class HTMLField(models.TextField):
    """This stores HTML content to be displayed raw to the user.
    The content is cleaned using bleach to restrict the set of HTML used.
    The TinyMCE widget is used for form editing."""
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, tags=None, attributes=None, *args, **kwargs):
        self.tags = tags
        self.attributes = attributes
        if tags is None:
            if hasattr(settings, 'ALLOWED_TAGS'):
                self.tags = settings.ALLOWED_TAGS
            else:
                self.tags = []
        if attributes is None:
            if hasattr(settings, 'ALLOWED_ATTRIBUTES'):
                self.attributes = settings.ALLOWED_ATTRIBUTES
            else:
                self.attributes = []
        return super(HTMLField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {'widget': TinyMCE()}
        defaults.update(kwargs)
        return super(HTMLField, self).formfield(**defaults)
    
    def to_python(self, value):
        value = super(HTMLField, self).to_python(value)
        value = bleach.clean(value, tags=self.tags, attributes=self.attributes, strip=True)
        value = bleach.linkify(value)
        return mark_safe(value)
    
try:
    from south.modelsinspector import add_introspection_rules
    rules = [
      (
        (HTMLField,),
        [],
        {
            "tags": ["tags", {"default": None}],
            "attributes": ["attributes", {"default": None}],
        },
      )
    ]
    add_introspection_rules(rules, ["^profiles\.fields\.HTMLField"])
except ImportError:
    pass
