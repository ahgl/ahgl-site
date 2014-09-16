import re
from django.forms import fields
from django.forms import ValidationError
from django.utils.encoding import smart_unicode

from django import forms
from django.db import models
 
class ColourFormField(forms.CharField):
    default_error_messages = {
        'invalid': 'Enter a valid colour value: e.g. "#ff0022"',
    }
    
    def __init__(self, *args, **kwargs):
        super(ColourFormField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        if value == '' and not self.required:
            return u''
 
        if not re.match('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
            raise forms.ValidationError(self.error_messages['invalid'])
        

        value = int(value[1:], 16)

        super(ColourFormField, self).clean(value)
 
        return value
 
class ColourField(models.CharField):
 
    description = "HEX value for a colour"
 
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(ColourField, self).__init__(*args, **kwargs)
 
    def to_python(self, value):
        super(ColourField, self).to_python(value)
 
        try:
            string = (hex(value)[2:]).zfill(6)
 
            if string == "0":
                string = "000000"
 
            return "#"+string.upper()
        except TypeError:
            return None
        
    def get_prep_value(self, value):
        try:
            return value
        except ValueError:
            return None
 
    def formfield(self, *args, **kwargs):
        kwargs['form_class'] = ColourFormField
 
        return super(ColourField, self).formfield(*args, **kwargs)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([
    (
        [ColourField],
        [],         
        {},
    ),
], ["^api\.fields\.ColourField"])

