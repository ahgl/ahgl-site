# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import DetailView, ListView, UpdateView
from django.forms import models as model_forms
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.template import RequestContext
from django.db.models import Count

from idios.views import ProfileDetailView
from idios.utils import get_profile_model

from utils.views import ObjectPermissionsCheckMixin
from .models import Team, TeamMembership
from apps.tournaments.models import TournamentRound, Tournament

class TournamentSlugContextView(object):
    def get_context_data(self, **kwargs):
        context = super(TournamentSlugContextView, self).get_context_data(**kwargs)
        context['tournament_slug'] = self.kwargs.get('tournament')
        """try:
            context['tournament'] = get_object_or_404(Tournament, slug=context['tournament_slug'])
        except Tournament.DoesNotExist:
            pass"""
        return context

class TeamDetailView(TournamentSlugContextView, DetailView):
    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context['is_captain'] = self.request.user.is_authenticated() and any((captain.profile.user_id==self.request.user.id for captain in self.object.captains))
        return context
        
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).select_related('charity')
    
class TeamUpdateView(ObjectPermissionsCheckMixin, UpdateView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).select_related('charity')
    
    def get_form_class(self):
        return model_forms.modelform_factory(Team, exclude=('slug','tournament','rank','seed','members',))
    
    def get_success_url(self):
        return reverse("team_page", kwargs=self.kwargs)

    def check_permissions(self):
        if not self.request.user.is_superuser and not self.object.team_membership.filter(captain=True, profile__user=self.request.user).count():
            return HttpResponseForbidden("You are not captain of this team.")
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamUpdateView, self).dispatch(*args, **kwargs)
    
class TeamListView(TournamentSlugContextView, ListView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).only('name','slug','photo','tournament')
    
class StandingsView(TournamentSlugContextView, ListView):
    def get_context_data(self, **kwargs):
        ctx = super(StandingsView, self).get_context_data(**kwargs)
        ctx["show_points"] = get_object_or_404(Tournament.objects.only('structure'), pk=self.kwargs['tournament']).structure=="I"
        return ctx
    
    def get_queryset(self):
        return TournamentRound.objects.filter(tournament=self.kwargs['tournament'], published=True)

    def get_template_names(self):
        return "profiles/standings.html"

class TeamMembershipUpdateView(ObjectPermissionsCheckMixin, UpdateView):
    template_name = "idios/profile_edit.html"
    template_name_ajax = "idios/profile_edit_ajax.html"
    template_name_ajax_success = "idios/profile_edit_ajax_success.html"
    context_object_name = "profile"
    form_class=model_forms.modelform_factory(TeamMembership, exclude=("team", "profile", "active", "captain",))
    model = TeamMembership
    
    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]
    def get_context_data(self, **kwargs):
        ctx = super(TeamMembershipUpdateView, self).get_context_data(**kwargs)
        ctx["profile_form"] = ctx["form"]
        return ctx
    
    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax():
            data = {
                "status": "success",
                "location": self.object.get_absolute_url(),
                "html": render_to_string(self.template_name_ajax_success),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            ctx = RequestContext(self.request, self.get_context_data(form=form))
            data = {
                "status": "failed",
                "html": render_to_string(self.template_name_ajax, ctx),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def check_permissions(self):
        if self.object.profile.user != self.request.user and not (self.object.profile.user.username=="master" and TeamMembership.objects.filter(profile__user=self.request.user, captain=True, team=self.object.team).count()):
            return HttpResponseForbidden("This is not your membership to edit.")
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamMembershipUpdateView, self).dispatch(*args, **kwargs)

class TeamMembershipView(TournamentSlugContextView, DetailView):
    template_name = "profiles/player_profile.html"
    context_object_name = "membership"
    def get_queryset(self):
        return TeamMembership.get(**self.kwargs)
    def get_context_data(self, **kwargs):
        ctx = super(TeamMembershipView, self).get_context_data(**kwargs)
        ctx['is_me'] = self.request.user.is_authenticated() and self.request.user.id == self.object.profile.user_id
        return ctx
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

class MVPView(TournamentSlugContextView, ListView):
    template_name = "profiles/mvp.html"
    context_object_name = "players"
    
    def get_queryset(self):
        return TeamMembership.objects.filter(team__tournament=self.kwargs.get('tournament'), game_wins__match__published=True).select_related('team','profile').annotate(win_count=Count('game_wins')).order_by('-win_count')

class MyProfileDetailView(ProfileDetailView):
    def get_object(self):
        queryset = get_profile_model().objects.select_related("user")
        slug = self.kwargs.get("slug")
        try:
            if slug:
                profile = get_object_or_404(queryset, slug=slug)
                self.page_user = profile.user
                return profile
        except:
            self.kwargs['username'] = slug
            return super(MyProfileDetailView, self).get_object()
    
