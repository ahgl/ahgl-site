# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, ListView, UpdateView
from django.forms import models as model_forms
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404

from idios.views import ProfileDetailView
from idios.utils import get_profile_model

from .models import Team
from apps.tournaments.models import TournamentRound

class TournamentSlugContextView(object):
    def get_context_data(self, **kwargs):
        context = super(TournamentSlugContextView, self).get_context_data(**kwargs)
        context['tournament_slug'] = self.kwargs.get('tournament')
        return context

class TeamDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context['tournament_slug'] = self.kwargs.get('tournament')
        return context
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).select_related('charity', 'captain')
    
class TeamUpdateView(UpdateView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).select_related('charity')
    
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
    
class TeamListView(TournamentSlugContextView, ListView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament'])
    
class StandingsView(TournamentSlugContextView, ListView):
    def get_queryset(self):
        return TournamentRound.objects.filter(tournament=self.kwargs['tournament'])

    def get_template_names(self):
        return "profiles/standings.html"
    
    
class MyProfileDetailView(ProfileDetailView):
    def get_object(self):
        profile_class = get_profile_model()
        slug = self.kwargs.get("slug")
        try:
            if slug:
                profile = get_object_or_404(profile_class, slug=slug)
                self.page_user = profile.user
                return profile
        except:
            self.kwargs['username'] = slug
            return super(MyProfileDetailView, self).get_object()
    
