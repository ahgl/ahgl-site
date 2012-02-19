# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, ListView, UpdateView
from django.forms import models as model_forms
from django.core.urlresolvers import reverse

from .models import Team
from apps.tournaments.models import TournamentRound

class TeamDetailView(DetailView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).select_related('charity', 'members')
    
class TeamUpdateView(UpdateView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament'])
    
    def get_form_class(self):
        return model_forms.modelform_factory(Team, exclude=('slug','tournament','rank','seed',))
    
    def get_success_url(self):
        return reverse("team_page", kwargs=self.kwargs)
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.object = self.get_object()
        if self.object.captain != request.user.get_profile():
            return HttpResponseForbidden("You are not captain of this team.")
        return super(TeamUpdateView, self).dispatch(request, *args, **kwargs)
    
class TeamListView(ListView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament'])
    
class StandingsView(ListView):
    def get_queryset(self):
        return TournamentRound.objects.filter(tournament=self.kwargs['tournament']).select_related('teams')

    def get_template_names(self):
        return "profiles/standings.html"