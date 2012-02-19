from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic import DetailView, ListView
from django.conf.urls.static import static
from django.forms import models as model_forms

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer
from idios.views import ProfileUpdateView
from messages.views import compose

from apps.profiles.models import Profile
from apps.profiles.views import TeamListView, TeamDetailView, StandingsView, TeamUpdateView
from apps.tournaments.views import TournamentDetailView, MatchDetailView, MatchListView, MatchReportView, MatchReportListView, SubmitLineupView, LineupView, MapListView
from apps.tournaments.models import Match, Tournament

handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r'^social/', include('social_auth.urls')),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/edit/$", ProfileUpdateView.as_view(form_class=model_forms.modelform_factory(Profile, exclude=('user','signature','signature_html','time_zone','language','post_count','avatar',))), name="profile_edit"),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^messages/compose/(?P<recipient>[\+\w\.]+)/$', compose, name='messages_compose_to'), #we allow periods
    url(r'^messages/', include('messages.urls')),
    url(r'^report_match/$', MatchReportListView.as_view(), name="report_match_list"),
    url(r'^report_match/(?P<pk>[\d]+)/$', MatchReportView.as_view(), name="report_match"),
    url(r'^submit_lineup/', SubmitLineupView.as_view(), name="submit_lineup"),
    url(r'^view_lineup/', LineupView.as_view(), name="view_lineup"),
    url(r'^map_list/', MapListView.as_view(), name="map_list"),
    url(r'^archive/$', ListView.as_view(queryset=Tournament.objects.filter(active=False), template_name="tournaments/archives.html"), name="archives"),
    url(r'^(?P<slug>[\w_-]+)/$', TournamentDetailView.as_view(), name='tournament'),
    url(r'^(?P<tournament>[\w_-]+)/teams/$', TeamListView.as_view(), name='teams'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<slug>[\w_-]+)/$', TeamDetailView.as_view(), name='team_page'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<slug>[\w_-]+)/edit/$', TeamUpdateView.as_view(), name='edit_team'),
    url(r'^(?P<tournament>[\w_-]+)/matches/$', MatchListView.as_view(), name='matches'),
    url(r'^matches/(?P<pk>[\d]+)/$', DetailView.as_view(model=Match), name='match_page'),
    #url(r'^(?P<tournament>[\w_-]+)/matches/(?P<date>[\d\\-]+)/(?P<home>[\w_-]+)-vs-(?P<away>[\w_-]+)$', MatchDetailView.as_view(), name='match_page'),
    url(r'^(?P<tournament>[\w_-]+)/standings/$', StandingsView.as_view(), name='standings'),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)