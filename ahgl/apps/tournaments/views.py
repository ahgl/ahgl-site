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
from django.http import Http404
from django.shortcuts import get_object_or_404
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
                self.instance.tournament_round = tournament_round
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
                            for i, map_form in enumerate(map_formset, start=1):
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
    queryset = Tournament.objects.all().select_related('featured_game__map', 'featured_game__home_player', 'featured_game__away_player')
    
class GameListView(ListView):
    template_name="tournaments/game_list.html"
    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        if self.request.GET.get('vod_only'):
            context['vod_only'] = True
        try:
            context['player'] = Profile.objects.get(slug=self.request.GET.get('player'))
        except Profile.DoesNotExist:
            pass
        else:
            wins, losses = [], []
            for game in self.object_list:
                if game.winner==context['player']:
                    wins.append(game)
                else:
                    losses.append(game)
            context['game_list'] = wins + losses
        return context
    def get_queryset(self):
        queryset = Game.objects.exclude(winner__isnull=True) \
                                       .order_by('match__publish_date', 'match', 'order') \
                                       .select_related('map', 'home_player', 'away_player', 'match__home_team', 'match__away_team', 'winner')
        if (not self.request.user.is_authenticated() or not self.request.user.get_profile().is_active()):
            queryset = queryset.filter(match__published=True)
        if self.request.GET.get('player'):
            queryset = queryset.filter(Q(home_player__slug=self.request.GET.get('player')) | Q(away_player__slug=self.request.GET.get('player')))
        if self.request.GET.get('vod_only'):
            queryset = queryset.filter(vod__isnull=False)
        return queryset
    
class MatchListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        context['tournament_slug'] = self.kwargs.get('tournament')
        return context

    def get_queryset(self):
        queryset = Match.objects.filter(tournament=self.kwargs['tournament']) \
                                       .order_by('publish_date', 'creation_date', 'tournament_round') \
                                       .select_related('home_team', 'away_team', 'tournament_round')
        if (not self.request.user.is_authenticated() or not self.request.user.get_profile().is_active(self.kwargs.get('tournament'))):
            queryset = queryset.filter(published=True)
        if self.request.GET.get('team'):
            queryset = queryset.filter(Q(home_team__slug=self.request.GET.get('team')) | Q(away_team__slug=self.request.GET.get('team')))
        return queryset

class MatchDetailView(DetailView):
    model=Match
    queryset=Match.objects.select_related('home_team', 'away_team')
    def get_context_data(self, **kwargs):
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        context['home_team_url'] = self.object.home_team.get_absolute_url(self.kwargs.get('tournament'))
        context['away_team_url'] = self.object.away_team.get_absolute_url(self.kwargs.get('tournament'))
        context['games_played'] = list(self.object.games_played())
        try:
            context['first_vod'] = context['games_played'][0].vod
        except IndexError:
            return context
        return context
    
    def get_object(self):
        return self.object
    
    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.object = super(MatchDetailView, self).get_object()
        if not self.object.published and (not request.user.is_authenticated() or not request.user.get_profile().is_active(self.kwargs.get('tournament'))):
            raise Http404
        return handler(request, *args, **kwargs)

class VerboseMatchDetailView(MatchDetailView): 
    def get_object(self):
        return Match.objects.filter(tournament=self.kwargs['tournament'],
                                    publish_date=self.kwargs['date'],
                                    home_team=self.kwargs['home'],
                                    away_team=self.kwargs['away']).select_related('home_team', 'away_team')

class MatchReportListView(ListView):
    model = Match
    template_name="tournaments/report_match_list.html"
    def get_queryset(self):
        return Match.objects.filter(home_submitted=True, away_submitted=True, published=False, tournament__teams__members__pk=self.request.user.get_profile().pk) \
                            .order_by('-creation_date') \
                            .select_related('home_team', 'away_team')
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MatchReportListView, self).dispatch(request, *args, **kwargs)

class MatchReportView(UpdateView):
    queryset = Match.objects.filter(home_submitted=True, away_submitted=True, published=False).select_related('home_team', 'away_team')
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
                    #TODO: figure out how to not issue a query since we know the exact set...maybe artificialy spoof a queryset object
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
        kwargs = {'instance':self.object, 'queryset':Game.objects.select_related('map', 'home_player__user', 'away_player__user')}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        self.object.referee = self.user
        self.object.remove_extra_victories()
        return super(MatchReportView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse("report_match_list")
    
    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        if not request.user.get_profile().teams.filter(tournament__matches__pk=pk).count():
            return HttpResponseForbidden("You are not a participant in this tournament.")
        self.user = request.user
        return super(MatchReportView, self).dispatch(request, pk=pk, *args, **kwargs)

class LineupView(ListView):
    model = Match
    def get_template_names(self):
        return "tournaments/view_lineup.html"
    def get_queryset(self):
        profile = self.request.user.get_profile()
        return Match.objects.filter(Q(home_submitted=True) & Q(away_submitted=True) & Q(published=False) & (Q(home_team__captain=profile) | Q(away_team__captain=profile))).select_related('home_team', 'away_team')
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LineupView, self).dispatch(request, *args, **kwargs)

class MapListView(ListView):
    model = Match
    def get_template_names(self):
        return "tournaments/map_list.html"
    def get_queryset(self):
        profile = self.request.user.get_profile()
        return Match.objects.filter(Q(published=False) & (Q(home_team__members__pk=profile.pk) | Q(away_team__members__pk=profile.pk))).distinct().select_related('home_team', 'away_team')
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MapListView, self).dispatch(request, *args, **kwargs)

class SubmitLineupView(UpdateView):
    def get_template_names(self):
        return "tournaments/submit_lineup.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitLineupView, self).get_context_data(**kwargs)
        if self.team:
            context['team'] = self.team
        context['aces'] = self.object.games.filter(is_ace=True).select_related('map')
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
            self.object.home_submitted = True
        else:
            self.object.away_submitted = True
        self.object.save()
        if notification and self.object.home_submitted and self.object.away_submitted:
            notification.send(User.objects.filter(profile__teams__pk__in=(self.object.home_team.pk, self.object.away_team.pk)),
                              "tournaments_lineup_ready",
                              {'match': self.object,
                               })
        return super(SubmitLineupView, self).form_valid(*args, **kwargs)
    
    def get_object(self):
        return self.object
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'instance':self.object, 'queryset':Game.objects.filter(is_ace=False).select_related('map')}
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
        submit_matchlist = Match.objects.filter((Q(home_submitted=False) | Q(away_submitted=False)) & Q(published=False) & (Q(home_team__captain=profile) | Q(away_team__captain=profile)))
        if not submit_matchlist.count():
            messages.add_message(request, messages.ERROR, "No lineups to submit.")
            self.request = request
            return self.render_to_response(context={})
        self.object = submit_matchlist[0]
        self.home_team = False
        if profile == self.object.home_team.captain:
            self.home_team = True
            self.team = self.object.home_team
        elif profile == self.object.away_team.captain:
            self.team = self.object.away_team
        return super(SubmitLineupView, self).dispatch(request, *args, **kwargs)
