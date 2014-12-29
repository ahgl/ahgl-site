from django.forms.models import BaseModelFormSet

from .models import Match, Game
from api.models import Character
from django.forms import ModelForm, ModelChoiceField

from django.utils.translation import ugettext_lazy as _


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

    def clean(self):
        super(GameForm, self).clean()
        from django.core.exceptions import ValidationError
        match = self.cleaned_data.get('match')
        home_race = self.cleaned_data.get('home_race')
        away_race = self.cleaned_data.get('away_race')

        if match:
            if home_race and home_race:
                # Check that the number of selected characters match to the character_number from api.Game
                if home_race.count() != match.tournament.game.character_number or away_race.count() != match.tournament.game.character_number:
                    raise ValidationError(_('Please, select %d characters for %s and %s fields') 
                        % (match.tournament.game.character_number, 
                            match.tournament.game.home_character_diplay_name, 
                            match.tournament.game.away_character_diplay_name))

        return self.cleaned_data

    class Meta:
        model = Game
        fields = ('map', 'order', 'home_player', 'home_race', 'away_player', 'away_race', 'winner', 
            'winner_team', 'forfeit', 'replay', 'vod', 'is_ace', 'victory_screen',)
