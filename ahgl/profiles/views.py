# Create your views here.
from warnings import warn

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django import forms
from django.forms import models as model_forms
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.template import RequestContext
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.db import IntegrityError
from django.contrib import messages

from idios.views import ProfileDetailView
from idios.utils import get_profile_model
from account.models import EmailAddress

from utils.views import ObjectPermissionsCheckMixin
from .models import Team, TeamMembership, Profile, Caster
from tournaments.models import TournamentRound, Tournament


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
        context['is_captain'] = self.request.user.is_authenticated() and any((captain.profile.user_id == self.request.user.id for captain in self.object.captains))
        return context

    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).select_related('charity')


class TeamUpdateView(ObjectPermissionsCheckMixin, TournamentSlugContextView, UpdateView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).select_related('charity')

    @property
    def requested_approval(self):
        return self.request.POST.get('submit') == 'approval'

    def get_form_class(self):
        view = self

        class UpdateForm(ModelForm):
            def __init__(self, *args, **kwargs):
                super(UpdateForm, self).__init__(*args, **kwargs)
                if view.requested_approval:
                    for key, field in self.fields.iteritems():
                        if key != 'approval':
                            field.required = True

            def clean_approval(self):
                value = self.cleaned_data.get('approval')
                if view.requested_approval:
                    if value:
                        self.instance.status = "W"
                    else:
                        raise forms.ValidationError("Approval from your company is required.")
                return value

            class Meta:
                model = Team
                exclude = ('slug', 'tournament', 'rank', 'seed', 'members', 'status', 'paid', 'karma',)
        return UpdateForm

    # Override this so we can save self.object for get_success_url.
    def form_valid(self, form):
        form.save()
        team = self.object = form.instance
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("edit_team", kwargs=self.kwargs)

    def check_permissions(self):
        if not self.request.user.is_superuser and not self.object.team_membership.filter(captain=True, profile__user=self.request.user).count():
            return HttpResponseForbidden("You are not captain of this team.")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamUpdateView, self).dispatch(*args, **kwargs)

class TeamSignupView(CreateView):
    model = Team

    def get_form_class(self):
        view = self

        class TeamSignupForm(ModelForm):
            char_name = forms.CharField(max_length=TeamMembership._meta.get_field('char_name').max_length,
                    required=True, label="Your character name", help_text=u"or Summoner name")

            def __init__(self, *args, **kwargs):
                super(TeamSignupForm, self).__init__(*args, **kwargs)
                # Limit tournament choices to those just in the signup stage.
                # via http://stackoverflow.com/q/291945/102704
                self.fields['tournament'].queryset = Tournament.objects.filter(status='S')

            class Meta:
                model = Team
                fields = [
                        'tournament',
                        'name', # Company name
                        'char_name',
                        ]

            def save(self, *args, **kwargs):
                view.slug = self.instance.slug = slugify(self.cleaned_data['name'])
                try:
                    super(TeamSignupForm, self).save(*args, **kwargs)
                except IntegrityError:
                    messages.error(view.request, "Team not created - already exists for this tournament.")
                else:
                    membership = TeamMembership(team=self.instance, profile=view.request.user.get_profile(), char_name=self.cleaned_data['char_name'], active=True, captain=True)
                    membership.save()
        return TeamSignupForm

    def get_success_url(self):
        return reverse("edit_team", kwargs={"tournament": self.request.POST['tournament'], "slug": self.slug})

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not EmailAddress.objects.filter(user=request.user, verified=True).count():
            return HttpResponseForbidden("Email verification required. Go here: http://afterhoursgaming.tv/account/settings/ enter your email and hit save. Then click the link in the email to verify. If you don't get an email, try changing it, saving, and changing it back.")
        return super(TeamSignupView, self).dispatch(request, *args, **kwargs)


class TeamAdminView(ListView):
    def get_queryset(self):
        return TeamMembership.objects.filter(profile__user=self.request.user, captain=True)

    def get_context_data(self, **kwargs):
        # Probably a better way to do this with joins, but I never remember how
        # to do that with Django. Sorry.
        team_ids = set(m.team_id for m in self.get_queryset()) # Why isn't this already in self.queryset?
        teams = Team.objects.filter(id__in=team_ids)
        memberships = TeamMembership.objects.filter(team_id__in=team_ids)
        return {
            'teams': teams,
            'memberships': memberships,
        }

    def get_template_names(self):
        return "profiles/team_admin.html"


class TeamListView(TournamentSlugContextView, ListView):
    def get_queryset(self):
        return Team.objects.filter(tournament=self.kwargs['tournament']).only('name', 'slug', 'photo', 'tournament')


class StandingsView(TournamentSlugContextView, ListView):
    def get_context_data(self, **kwargs):
        ctx = super(StandingsView, self).get_context_data(**kwargs)
        ctx["show_points"] = get_object_or_404(Tournament.objects.only('structure'), pk=self.kwargs['tournament']).structure == "I"
        return ctx

    def get_queryset(self):
        return TournamentRound.objects.filter(tournament=self.kwargs['tournament'], published=True)

    def get_template_names(self):
        return "profiles/standings.html"


class TeamMembershipCreateView(CreateView):
    model = TeamMembership
    template_name = "profiles/membership_form.html"
    context_object_name = "membership"

    def get_form_class(self):
        view = self

        class MembershipCreateForm(ModelForm):
            team = forms.ModelChoiceField(queryset=Team.objects.filter(team_membership__profile__user=view.request.user))
            profile = forms.ModelChoiceField(queryset=Profile.objects.filter(slug=self.kwargs['slug']), initial=view.profile, widget=forms.HiddenInput())

            class Meta:
                model = TeamMembership
                fields = ('char_name', 'team', 'profile')

            def save(self, *args, **kwargs):
                self.cleaned_data['profile'] = view.profile
                return super(MembershipCreateForm, self).save(*args, **kwargs)
        return MembershipCreateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, slug=kwargs['slug'])
        return super(TeamMembershipCreateView, self).dispatch(request, *args, **kwargs)


class TeamMembershipUpdateView(ObjectPermissionsCheckMixin, UpdateView):
    template_name = "idios/profile_edit.html"
    template_name_ajax = "idios/profile_edit_ajax.html"
    template_name_ajax_success = "idios/profile_edit_ajax_success.html"
    context_object_name = "profile"
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

    def get_form_class(self):
        exclude = ["team", "profile"]
        if not self.captain_user:
            exclude += ["captain", "active"]
        return model_forms.modelform_factory(TeamMembership, exclude=exclude)

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
        self.captain_user = bool(TeamMembership.objects.filter(team=self.object.team, profile__user=self.request.user, captain=True).count())
        if self.object.profile.user != self.request.user and not self.captain_user:
            return HttpResponseForbidden("This is not your membership to edit.")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamMembershipUpdateView, self).dispatch(*args, **kwargs)


class TeamMembershipDeleteView(ObjectPermissionsCheckMixin, DeleteView):
    context_object_name = "profile"
    model = TeamMembership

    def get_success_url(self):
        return reverse("team_page", kwargs={"tournament": self.object.team.tournament.slug, "slug": self.object.team.slug})

    def check_permissions(self):
        self.captain_user = bool(TeamMembership.objects.filter(team=self.object.team, profile__user=self.request.user, captain=True).count())
        if self.object.profile.user != self.request.user and not self.captain_user:
            return HttpResponseForbidden("This is not your membership to delete.")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TeamMembershipDeleteView, self).dispatch(*args, **kwargs)


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
        return TeamMembership.objects.filter(team__tournament=self.kwargs.get('tournament'), game_wins__match__published=True).select_related('team', 'profile').annotate(win_count=Count('game_wins')).order_by('-win_count')


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


class CasterListView(ListView):
    template_name = "profiles/casters.html"
    context_object_name = "casters"

    def get_queryset(self):
        return Caster.objects.filter(tournament=self.kwargs.get('tournament')).order_by('-active', '?')
