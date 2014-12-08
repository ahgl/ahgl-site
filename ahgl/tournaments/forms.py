from django.forms.models import BaseModelFormSet

from .models import Match, Game
from api.models import Character
from django.forms import ModelForm, ModelChoiceField


class BaseMatchFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseMatchFormSet, self).__init__(*args, **kwargs)
        self.queryset = Match.objects.none()

    def get_queryset(self):
        return Match.objects.none()


class MultipleFormSetBase(object):
    def __init__(self, prefix=None, *args, **kwargs):
        if prefix is None:
            prefix = ''
        self.forms = [form_class(prefix=prefix + form_prefix, *args, **kwargs)
                      for i, (form_prefix, form_class) in enumerate(self.form_classes.iteritems())]

    def __unicode__(self):
        return self.as_table()

    def __iter__(self):
        for formset in self.forms:
            yield formset
            #for field in form:
            #    yield field

    def is_valid(self):
        return all(form.is_valid() for form in self.forms)

    def as_table(self):
        return '\n'.join(form.as_table() for form in self.forms)

    def as_ul(self):
        return '\n'.join(form.as_ul() for form in self.forms)

    def as_p(self):
        return '\n'.join(form.as_p() for form in self.forms)

    def is_multipart(self):
        return any(form.is_multipart() for form in self.forms)

    def save(self, commit=True):
        return tuple(form.save(commit) for form in self.forms if hasattr(form, "save"))
    save.alters_data = True

class GameForm(ModelForm):
    """Form for adding and editing games."""
    
    def __init__(self, *args, **kwargs):
        super(GameForm,self).__init__(*args,**kwargs)
        # TODO: For some reason accessing self.instance raises some issues
        if self.instance:
            self.fields['home_race'].label = self.instance.match.tournament.game.home_character_diplay_name
            self.fields['away_race'].label = self.instance.match.tournament.game.away_character_diplay_name

    class Meta:
        model = Game
