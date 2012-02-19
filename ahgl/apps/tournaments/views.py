# Create your views here.
import logging

from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.detail import TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.forms.models import inlineformset_factory, modelformset_factory
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.forms import ModelForm, BaseModelForm
from django.forms.models import BaseModelFormSet
from django import forms
from django.forms.models import ModelFormOptions
from django.forms.formsets import formset_factory
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
from django.utils.datastructures import SortedDict

from apps.profiles.models import Profile, RACES

from .models import Tournament, Map, Match, Game, TournamentRound
from .forms import BaseMatchFormSet, MultipleFormSetBase

logger = logging.getLogger(__name__)


class NewTournamentRoundView(TemplateResponseMixin, FormMixin, ProcessFormView):
    template_name = "admin/tournaments/tournament/new_round.html"
    def get_success_url(self):
        return reverse("admin:tournaments_match_changelist")
    def map_selection_form(self):
        tournament = self.tournament
        class MapSelectionForm(forms.Form):
            map = forms.ModelChoiceField(queryset=tournament.map_pool.all(), required=True)
            is_ace = forms.BooleanField(initial=False, required=False)
        return MapSelectionForm
    def team_selection_form(self, tournament_round):
        tournament = self.tournament
        class TeamSelectionForm(ModelForm):
            home_team = forms.ModelChoiceField(queryset=tournament_round.teams.all(), required=True)
            away_team = forms.ModelChoiceField(queryset=tournament_round.teams.all(), required=True)
            class Meta:
                model = Match
                fields = ('home_team', 'away_team', )
            def clean(self):
                if self.cleaned_data.get('home_team') == self.cleaned_data.get('away_team'):
                    raise forms.ValidationError("Teams cannot battle themselves")
                return super(TeamSelectionForm, self).clean()
            def save(self, *args, **kwargs):
                self.instance.tournament = tournament
                return super(TeamSelectionForm, self).save(*args, **kwargs)
        return TeamSelectionForm
        
    def get_form_class(self):
        tournament = self.tournament
        stage = self.stage
        map_form_class = [('Maps',formset_factory(self.map_selection_form(), extra=tournament.games_per_match))]
        match_form_classes = [("Division "+tournament_round.name, modelformset_factory(Match, formset=BaseMatchFormSet, form=self.team_selection_form(tournament_round), extra=tournament_round.teams.count()//2))
                              for tournament_round in self.tournament_rounds]
        class NewTournamentRoundForm(MultipleFormSetBase):
            form_classes = SortedDict(map_form_class+match_form_classes)
            def __init__(self, *args, **kwargs):
                super(NewTournamentRoundForm, self).__init__(*args, **kwargs)
                self.maps_formset = self.forms[0]
                self.match_formsets = self.forms[1:]
                if len(self.maps_formset.forms) > 1:
                    self.maps_formset.forms[-1].fields['is_ace'].initial=True
            def save(self, *args, **kwargs):
                ret = super(NewTournamentRoundForm, self).save(*args, **kwargs)
                map_formset = self.forms[0]
                for match_formset in self.forms[1:]:
                    for match_form in match_formset:
                        if match_form.instance.id:
                            for i, map_form in enumerate(map_formset):
                                if 'map' in map_form.cleaned_data:
                                    match_form.instance.games.create(order=i, **map_form.cleaned_data)
                return ret
        return NewTournamentRoundForm
    
    def form_valid(self, form):
        self.object = form.save()
        return super(NewTournamentRoundView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        kwargs = super(NewTournamentRoundView, self).get_context_data(**kwargs)
        kwargs['tournament'] = self.tournament
        kwargs['stage'] = self.stage
        kwargs['tournament_rounds'] = self.tournament_rounds
        return kwargs
    
    def dispatch(self, request, *args, **kwargs):
        self.stage = int(kwargs.get('stage') or request.GET.get('stage'))
        self.tournament = Tournament.objects.get(slug=kwargs.get('tournament'))
        self.tournament_rounds = TournamentRound.objects.filter(tournament=self.tournament, stage=self.stage)
        return super(NewTournamentRoundView, self).dispatch(request, *args, **kwargs)


class TournamentDetailView(DetailView):
    queryset = Tournament.objects.all()
    
class MatchListView(ListView):
    def get_queryset(self):
        return Match.objects.filter(tournament=self.kwargs['tournament'], published=True).order_by('publish_date')

class MatchDetailView(ListView):
    def get_object(self):
        return Match.objects.filter(tournament=self.kwargs['tournament'],
                                    publish_date=self.kwargs['date'],
                                    home_team=self.kwargs['home'],
                                    away_team=self.kwargs['away'])

class MatchReportListView(ListView):
    model = Match
    template_name="tournaments/report_match_list.html"
    def get_queryset(self):
        return Match.objects.filter(home_submitted=True, away_submitted=True, published=False, tournament__teams__members__pk=self.request.user.get_profile().pk)
    
class MatchReportView(UpdateView):
    queryset = Match.objects.filter(home_submitted=True, away_submitted=True, published=False)
    template_name = "tournaments/report_match.html"
    
    def get_form_class(self):
        match = self.object
        class ReportMatchForm(ModelForm):
            winner = forms.ModelChoiceField(required=False,
                                            queryset=Profile.objects.all(),
                                            widget=forms.RadioSelect,
                                            empty_label="Not played")
            home_player = forms.ModelChoiceField(required=False, queryset=Profile.objects.filter(teams__pk=match.home_team.pk))
            away_player = forms.ModelChoiceField(required=False, queryset=Profile.objects.filter(teams__pk=match.away_team.pk))
            
            def __init__(self, *args, **kwargs):
                super(ReportMatchForm, self).__init__(*args, **kwargs)
                winner_field = self.fields.get('winner')
                if not self.instance.is_ace:
                    assert(self.instance.home_player and self.instance.away_player)
                    winner_field.queryset = winner_field.queryset.filter(pk__in=(self.instance.home_player.pk, self.instance.away_player.pk,))
                    winner_field.choices = (("", "Not played"), (self.instance.home_player.pk, str(self.instance.home_player)), (self.instance.away_player.pk, str(self.instance.away_player)))
                    del self.fields['home_player']
                    del self.fields['home_race']
                    del self.fields['away_player']
                    del self.fields['away_race']
                else:
                    winner_field.queryset = winner_field.queryset.filter(teams__pk__in=(match.home_team.pk,match.away_team.pk,))
                    #winner_field.widget = forms.Select
            class Meta:
                model = Game
                fields=('replay','home_player','home_race','away_player','away_race','winner','forfeit',)
        return inlineformset_factory(Match, Game, extra=0, can_delete=False, form=ReportMatchForm)
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'instance':self.get_object(), 'queryset':Game.objects.all()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs
    
    def get_success_url(self):
        return reverse("report_match_list")
    
    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        if not request.user.get_profile().teams.filter(tournament__matches__pk=pk).count():
            return HttpResponseForbidden("You are not a participant in this tournament.")
        return super(MatchReportView, self).dispatch(request, pk=pk, *args, **kwargs)

class LineupView(ListView):
    model = Match
    def get_template_names(self):
        return "tournaments/view_lineup.html"
    def get_queryset(self):
        profile = self.request.user.get_profile()
        return Match.objects.filter(Q(home_submitted=True) & Q(away_submitted=True) & Q(published=False) & (Q(home_team__captain=profile) | Q(away_team__captain=profile)))

class MapListView(ListView):
    model = Match
    def get_template_names(self):
        return "tournaments/map_list.html"
    def get_queryset(self):
        profile = self.request.user.get_profile()
        return Match.objects.filter(Q(published=False) & (Q(home_team__members__pk=profile.pk) | Q(away_team__members__pk=profile.pk))).all()

class SubmitLineupView(UpdateView):
    def get_template_names(self):
        return "tournaments/submit_lineup.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitLineupView, self).get_context_data(**kwargs)
        if self.team:
            context['team'] = self.team
        context['aces'] = Game.objects.filter(match=self.obj, is_ace=True)
        return context

    def get_form_class(self):
        if self.home_team:
            side = "home"
        else:
            side = "away"
        player = forms.ModelChoiceField(queryset=Profile.objects.filter(teams__pk=self.team.pk), label='Player')
        race = forms.ChoiceField(label='Race', choices=[('','---------')]+list(RACES))
        namespace = {'base_fields':{side+'_player': player, side+'_race': race},
                     '_meta':ModelFormOptions({'model':Game,
                                               'fields':(side+'_player', side+'_race', )
                                               })
                     }
        form = type('SubmitLineupForm', (BaseModelForm,), namespace)
        return inlineformset_factory(Match, Game, extra=0, can_delete=False, form=form)
    
    def form_valid(self, *args, **kwargs):
        if self.home_team:
            self.obj.home_submitted = True
        else:
            self.obj.away_submitted = True
        self.obj.save()
        if notification and self.obj.home_submitted and self.obj.away_submitted:
            notification.send(User.objects.filter(profile__teams__pk__in=(self.obj.home_team.pk, self.obj.away_team.pk)),
                              "tournaments_lineup_ready",
                              {'match': self.obj,
                               })
        return super(SubmitLineupView, self).form_valid(*args, **kwargs)
    
    def get_object(self):
        return self.obj
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'instance':self.get_object(), 'queryset':Game.objects.filter(is_ace=False)}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs
    
    def get_success_url(self):
        return reverse("view_lineup")
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        profile = request.user.get_profile()
        submit_matchlist = Match.objects.filter((Q(home_submitted=False) | Q(away_submitted=False)) & Q(published=False) & (Q(home_team__captain=profile) | Q(away_team__captain=profile))).all()
        if not submit_matchlist.count():
            messages.add_message(request, messages.ERROR, "No lineups to submit.")
            self.request = request
            return self.render_to_response(context={})
        self.obj = submit_matchlist[0]
        self.home_team = False
        if profile == self.obj.home_team.captain:
            self.home_team = True
            self.team = self.obj.home_team
        elif profile == self.obj.away_team.captain:
            self.team = self.obj.away_team
        return super(SubmitLineupView, self).dispatch(request, *args, **kwargs)
