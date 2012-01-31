# Create your views here.
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
#from django.account.models import User

from django.forms import ModelForm
from django import forms
from apps.profiles.models import Profile, RACES
from notification import models as notification

from models import Tournament, Map, Match, Game, GAME_OUTCOME

class TournamentDetailView(DetailView):
    pass
    
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
        winner_choices = (
                          ("H", self.get_object().home_team.name),
                          ("A", self.get_object().away_team.name),
                          ("N", "Not played"),
                          )
        class ReportMatchForm(ModelForm):
            winner = forms.ChoiceField(required=False, choices = winner_choices, widget=forms.RadioSelect)
            class Meta:
                model = Game
                fields=('replay','winner','forfeit',)
        return inlineformset_factory(Match, Game, extra=0, can_delete=False, form=ReportMatchForm)
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'instance':self.get_object(), 'queryset':Game.objects.order_by('order')}
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

class SubmitLineupView(UpdateView):
    def get_template_names(self):
        return "tournaments/submit_lineup.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitLineupView, self).get_context_data(**kwargs)
        if self.team:
            context['team'] = self.team
        context['aces'] = Game.objects.filter(match=self.obj, is_ace=True).order_by('order')
        return context

    def get_form_class(self):
        player = forms.ModelChoiceField(queryset=Profile.objects.filter(teams__pk=self.team.pk), label='Player')
        race = forms.ChoiceField(label='Race', choices=[('','---------')]+list(RACES))
        class SubmitLineupFormAway(ModelForm):
            away_player = player
            away_race = race
            class Meta:
                model = Game
                fields = ('away_player', 'away_race', )
        class SubmitLineupFormHome(ModelForm):
            home_player = player
            home_race = race
            class Meta:
                model = Game
                fields = ('home_player', 'home_race', )
        if self.home_team:
            form = SubmitLineupFormHome
        else:
            form = SubmitLineupFormAway
        return inlineformset_factory(Match, Game, extra=0, can_delete=False, form=form)
    
    def form_valid(self, *args, **kwargs):
        if self.home_team:
            self.obj.home_submitted = True
        else:
            self.obj.away_submitted = True
        self.obj.save()
        #TODO: send fancy notification that lineup is ready
        """if self.obj.home_submitted and self.obj.away_submitted:
            notification.send(User.objects.filter(), "lineup_ready", "Lineup is ready.", [])"""
        return super(SubmitLineupView, self).form_valid(*args, **kwargs)
    
    def get_object(self):
        return self.obj
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'instance':self.get_object(), 'queryset':Game.objects.filter(is_ace=False).order_by('order')}
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