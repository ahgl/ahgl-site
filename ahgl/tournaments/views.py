# Create your views here.
import logging

from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.detail import TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.forms.models import inlineformset_factory, modelformset_factory, modelform_factory
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ModelForm, BaseModelForm
from django import forms
from django.forms.models import ModelFormOptions
from django.forms.formsets import formset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.admin import widgets
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None
from django.utils.datastructures import SortedDict

from utils.views import ObjectPermissionsCheckMixin
from profiles.models import Profile, RACES, TeamMembership, Team
from profiles.views import TournamentSlugContextView

from .models import Tournament, Match, Game, TournamentRound
from .forms import BaseMatchFormSet, MultipleFormSetBase

from api.models import Character
from .forms import GameForm

logger = logging.getLogger(__name__)


class NewTournamentRoundView(TemplateResponseMixin, FormMixin, ProcessFormView):
    """Admin tool for batch match creation"""
    template_name = "admin/tournaments/tournament/new_round.html"

    def get_success_url(self):
        return reverse("admin:tournaments_match_changelist")

    def map_selection_form(self):
        tournament = self.tournament

        class MapSelectionForm(forms.Form):
            map = forms.ModelChoiceField(queryset=tournament.map_pool.all(), required=False)
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

    def global_form(self):
        class GlobalForm(forms.Form):
            play_date = forms.DateTimeField(widget=widgets.AdminSplitDateTime(), required=True)
            structure = forms.ChoiceField(initial=self.tournament.structure, choices=Match._meta.get_field('structure').choices)
        return GlobalForm

    def get_form_class(self):
        tournament = self.tournament
        global_form_class = [('Global Data', formset_factory(self.global_form()))]
        map_form_class = [('Maps', formset_factory(self.map_selection_form(), extra=tournament.games_per_match))]

        match_form_classes = [("Division " + str(tournament_round.order), modelformset_factory(Match, formset=BaseMatchFormSet, form=self.team_selection_form(tournament_round), extra=tournament_round.teams.count() // 2))
                              for tournament_round in self.tournament_rounds]

        class NewTournamentRoundForm(MultipleFormSetBase):
            form_classes = SortedDict(global_form_class + map_form_class + match_form_classes)

            def __init__(self, *args, **kwargs):
                super(NewTournamentRoundForm, self).__init__(*args, **kwargs)
                self.maps_formset = self.forms[1]
                self.match_formsets = self.forms[2:]
                if len(self.maps_formset.forms) > 1:
                    self.maps_formset.forms[-1].fields['is_ace'].initial = True

            def save(self, *args, **kwargs):
                date = self.forms[0].forms[0].cleaned_data.get('play_date', timezone.now())
                structure = self.forms[0].forms[0].cleaned_data.get('structure', tournament.structure)
                for match_formset in self.forms[2:]:
                    for match_form in match_formset:
                        match_form.instance.creation_date = date
                        match_form.instance.structure = structure
                if structure == "T":  # Team games don't need to submit lineup, so skip this stage
                    for match_formset in self.forms[2:]:
                        for match_form in match_formset:
                            match_form.instance.home_submitted = True
                            match_form.instance.away_submitted = True
                ret = super(NewTournamentRoundForm, self).save(*args, **kwargs)
                map_formset = self.forms[1]
                for match_formset in self.forms[2:]:
                    for match_form in match_formset:
                        if match_form.instance.id:
                            for i, map_form in enumerate(map_formset, start=1):
                                if 'map' in map_form.cleaned_data and map_form.cleaned_data['map']:
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
        self.tournament = get_object_or_404(Tournament, slug=kwargs.get('tournament'))
        self.tournament_rounds = TournamentRound.objects.filter(tournament=self.tournament, stage_order=self.stage)
        return super(NewTournamentRoundView, self).dispatch(request, *args, **kwargs)


class GameListView(TournamentSlugContextView, ListView):
    template_name = "tournaments/game_list.html"
    vod_only = False

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        if self.vod_only or self.request.GET.get('vod_only'):
            context['vod_only'] = True
        is_win = None
        if hasattr(self, 'member'):
            context['member'] = context['player'] = self.member
            is_win = lambda game: game.winner_id == self.member.pk
        elif hasattr(self, 'player'):
            context['profile'] = context['player'] = self.player
            is_win = lambda game: game.winner and game.winner.profile_id == self.player.pk
        if is_win:
            context['game_list'] = list(self.object_list)
            context['game_list'].sort(key=is_win, reverse=True)
        return context

    def get_queryset(self):
        related_members = ['map', 'home_player__profile',
                           'away_player__profile', 'home_player__team',
                           'away_player__team', 'match__home_team',
                           'match__away_team']
        used_fields = Game.fields_for_game_detail + [
            'match__home_team__name',
            'match__home_team__photo',
            'match__away_team__name',
            'match__away_team__photo',
            'match__creation_date',
            'match__publish_date',
            'match__home_submitted',
            'match__away_submitted',
        ]
        queryset = (Game.objects.exclude(winner_team__isnull=True)
                    .order_by('match__publish_date', 'match', 'order'))
        if (not self.request.user.is_authenticated() or not self.request.user.get_profile().is_active()):
            queryset = queryset.filter(match__published=True)
        if self.kwargs.get('tournament'):
            queryset = queryset.filter(match__tournament=self.kwargs.get('tournament'))
        if self.kwargs.get('team') and self.kwargs.get('profile'):
            self.member = get_object_or_404(TeamMembership.get(**self.kwargs).only('profile__slug', 'team__slug', 'team__tournament', 'char_name'))
            queryset = queryset.filter(Q(home_player=self.member) | Q(away_player=self.member))
        else:
            if self.request.GET.get('player'):
                queryset = queryset.filter(Q(home_player__profile__slug=self.request.GET.get('player')) | Q(away_player__profile__slug=self.request.GET.get('player')))
                related_members.append('winner')
                try:
                    self.player = Profile.objects.get(slug=self.request.GET.get('player'))
                except Profile.DoesNotExist:
                    pass
            elif self.request.GET.get('s'):  # using the search field
                queryset = queryset.filter(Q(home_player__char_name__icontains=self.request.GET.get('s'))
                                           | Q(home_player__profile__name__icontains=self.request.GET.get('s'))
                                           | Q(away_player__char_name__icontains=self.request.GET.get('s'))
                                           | Q(away_player__profile__name__icontains=self.request.GET.get('s'))
                                           )
        if self.vod_only or self.request.GET.get('vod_only'):
            queryset = queryset.exclude(vod="").order_by('-match__publish_date', 'match', 'order')
        return queryset.select_related(*related_members).only(*used_fields)


class MatchListView(TournamentSlugContextView, ListView):
    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        context['team_slug'] = self.kwargs.get('team')
        return context

    def get_queryset(self):
        queryset = (Match.objects.filter(tournament=self.kwargs['tournament'])
                    .order_by('publish_date', 'creation_date', 'tournament_round')
                    .select_related('home_team', 'away_team', 'tournament_round'))
        if (not self.request.user.is_authenticated() or not self.request.user.get_profile().is_active(self.kwargs.get('tournament'))):
            queryset = queryset.filter(published=True)
        team = self.kwargs.get('team') or self.request.GET.get('team')
        if team:
            queryset = queryset.filter(Q(home_team__slug=team) | Q(away_team__slug=team))
        return queryset

class MatchDetailView(ObjectPermissionsCheckMixin, TournamentSlugContextView, DetailView):
    model = Match
    queryset = Match.objects.select_related('home_team', 'away_team')

    def get_context_data(self, **kwargs):
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        context['games'] = list(self.object.games_played()) if self.object.published else list(self.object.games_with_related())
        try:
            context['first_vod'] = context['games'][0].vod
        except IndexError:
            return context
        if "blip.tv/play" not in context['first_vod']:
            del context['first_vod']
        return context

    def check_permissions(self):
        if not self.object.published and (not self.request.user.is_authenticated() or not self.request.user.get_profile().is_active(self.kwargs.get('tournament'))):
            raise Http404


class VerboseMatchDetailView(MatchDetailView):
    def get_object(self):
        return Match.objects.filter(tournament=self.kwargs['tournament'],
                                    publish_date=self.kwargs['date'],
                                    home_team=self.kwargs['home'],
                                    away_team=self.kwargs['away']).select_related('home_team', 'away_team')


############## Player admin tools follow ###############

class PlayerAdminView(ListView):
    model = Match
    template_name = "tournaments/player_admin.html"
    context_object_name = "report_match_list"

    def get_context_data(self, **kwargs):
        context = super(PlayerAdminView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['team_matches'] = self.match_list
        else:
            teams = Team.objects.filter(members__user=self.request.user)
            context['team_matches'] = self.match_list.filter(Q(home_team__in=teams)
                                                             | Q(away_team__in=teams))
        return context

    def get_queryset(self):
        self.match_list = (Match.objects.filter(published=False)
                           .order_by('-creation_date')
                           .select_related('home_team', 'away_team'))
        if not self.request.user.is_superuser:
            self.match_list = self.match_list.filter(tournament__teams__members__user=self.request.user)
        return self.match_list.filter(home_submitted=True, away_submitted=True)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PlayerAdminView, self).dispatch(request, *args, **kwargs)


class MatchReportView(UpdateView):
    #TODO: prefetch related
    queryset = Match.objects.filter(home_submitted=True, away_submitted=True, published=False).select_related('home_team', 'away_team', 'tournament')
    template_name = "tournaments/report_match.html"

    def get_form_class(self):
        match = self.object
        if match.structure == "I":
            class ReportMatchForm(GameForm):
                winner = forms.ModelChoiceField(required=False,
                                                queryset=TeamMembership.objects.all(),
                                                widget=forms.RadioSelect,
                                                empty_label="Not played")
                home_player = forms.ModelChoiceField(required=False, queryset=TeamMembership.objects.filter(team=match.home_team, active=True))
                away_player = forms.ModelChoiceField(required=False, queryset=TeamMembership.objects.filter(team=match.away_team, active=True))

                def __init__(self, *args, **kwargs):
                    super(ReportMatchForm, self).__init__(*args, **kwargs)
                    winner_field = self.fields.get('winner')
                    if not self.instance.is_ace:
                        assert(self.instance.home_player and self.instance.away_player)
                        #TODO: figure out how to not issue a query since we know the exact set...maybe artificialy spoof a queryset object
                        winner_field.queryset = winner_field.queryset.filter(pk__in=(self.instance.home_player_id, self.instance.away_player_id,))
                        winner_field.choices = (("", "Not played"), (self.instance.home_player_id, str(self.instance.home_player)), (self.instance.away_player_id, str(self.instance.away_player)))
                        del self.fields['home_player']
                        del self.fields['home_race']
                        del self.fields['away_player']
                        del self.fields['away_race']
                    else:
                        self.fields['winner'] = forms.ModelChoiceField(required=False,
                                                                       queryset=TeamMembership.objects.filter(active=True, team__pk__in=(match.home_team_id, match.away_team_id,)),
                                                                       empty_label="Not played"
                                                                       )
                        
                        characters = Character.objects.filter(game=match.tournament.game)
                        self.fields['home_race'] = forms.ModelMultipleChoiceField(required=False,
                                                                                  queryset=characters)
                        self.fields['away_race'] = forms.ModelMultipleChoiceField(required=False,
                                                                                  queryset=characters)

                        if match.tournament.game:
                            self.fields['home_race'].label = match.tournament.game.home_character_diplay_name
                            self.fields['away_race'].label = match.tournament.game.away_character_diplay_name

                class Meta:
                    model = Game
                    fields = ('replay', 'home_player', 'home_race', 'away_player', 'away_race', 'winner', 'forfeit',)
        else:
            class ReportMatchForm(ModelForm):
                winner_team = forms.ModelChoiceField(required=False,
                                                     queryset=Team.objects.all(),
                                                     widget=forms.RadioSelect,
                                                     empty_label="Not played")

                def __init__(self, *args, **kwargs):
                    super(ReportMatchForm, self).__init__(*args, **kwargs)
                    winner_field = self.fields.get('winner_team')
                    winner_field.queryset = winner_field.queryset.filter(pk__in=(match.home_team_id, match.away_team_id,)).only('name')

                class Meta:
                    model = Game
                    fields = ('replay', 'victory_screen', 'winner_team', 'forfeit')
        ReportMatchForm.queryset = Game.objects.select_related('map', 'home_player', 'away_player')
        form_classes = SortedDict([("Games", inlineformset_factory(Match, Game, extra=0, can_delete=False, form=ReportMatchForm)),
                                   ("Match", modelform_factory(Match, fields=('description',)))])
        return type("MatchReportForm", (MultipleFormSetBase,),
                    {"form_classes": form_classes})

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'instance': self.object}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        self.object.referee = self.user.get_profile()
        self.object.remove_extra_victories()
        messages.success(self.request, 'Result submission successful.')
        return super(MatchReportView, self).form_valid(form)

    def get_success_url(self):
        return reverse("player_admin")

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser and not request.user.get_profile().teams.filter(tournament__matches__pk=pk).count():
            return HttpResponseForbidden("You are not a participant in this tournament.")
        self.user = request.user
        return super(MatchReportView, self).dispatch(request, pk=pk, *args, **kwargs)


class SubmitLineupView(ObjectPermissionsCheckMixin, UpdateView):
    template_name = "tournaments/submit_lineup.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitLineupView, self).get_context_data(**kwargs)
        if self.team:
            context['team'] = self.team
        context['aces'] = self.object.games.filter(is_ace=True).select_related('map')
        return context

    def get_form_class(self):
        team = self.team
        match = self.object
        race_label = None
        if self.home_team:
            side = "home"
            if match.tournament.game:
                race_label = match.tournament.game.home_character_diplay_name
        else:
            side = "away"
            if match.tournament.game:
                race_label = match.tournament.game.away_character_diplay_name

        class SubmitLineupForm(GameForm):
            def __init__(self, *args, **kwargs):
                super(SubmitLineupForm, self).__init__(*args, **kwargs)

                queryset = TeamMembership.objects.filter(team=team, active=True)

                self.fields[side + '_player'] = forms.ModelChoiceField(queryset=TeamMembership.objects.filter(team=team, active=True),
                                                                        label='%s Player' % (side.title()))
                self.fields[side + '_race'] = forms.ModelMultipleChoiceField(queryset=Character.objects.filter(game=match.tournament.game))

                if race_label:
                    self.fields[side + '_race'].label = race_label

            class Meta:
                model = Game
                fields = (side + '_player', side + '_race')

        return inlineformset_factory(Match, Game, extra=0, can_delete=False, form=SubmitLineupForm)

    def form_valid(self, *args, **kwargs):
        if self.home_team:
            # upon first submission, set date
            if not self.object.home_submission_date:
                self.object.home_submission_date = timezone.now()
            self.object.home_submitted = True
        else:
            # upon first submission, set date
            if not self.object.away_submission_date:
                self.object.away_submission_date = timezone.now()
            self.object.away_submitted = True
        self.object.save()
        if notification and self.object.home_submitted and self.object.away_submitted:
            notification.send(User.objects.exclude(username='master').filter(profile__teams__pk__in=(self.object.home_team_id, self.object.away_team_id)),
                              "tournaments_lineup_ready",
                              {'match': self.object})
        messages.success(self.request, 'Lineup submission successful.')
        return super(SubmitLineupView, self).form_valid(*args, **kwargs)

    def get_queryset(self):
        return Match.objects.filter((Q(home_submitted=False) | Q(away_submitted=False)) & Q(published=False)).select_related('home_team', 'away_team')

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {
            'instance': self.object,
            'queryset': Game.objects.filter(is_ace=False).select_related('map')
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        return reverse("player_admin")

    def check_permissions(self):
        self.captain_teams = [role.team_id for role in TeamMembership.objects.filter(profile__user=self.request.user, captain=True)]
        if self.object.home_team_id in self.captain_teams:
            self.home_team = True
            self.team = self.object.home_team
        elif self.object.away_team_id in self.captain_teams or self.request.user.is_superuser:
            self.home_team = False
            self.team = self.object.away_team
        else:
            return HttpResponseForbidden("You are not captain of either of the teams in this match.")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SubmitLineupView, self).dispatch(request, *args, **kwargs)
