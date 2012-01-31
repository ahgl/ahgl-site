from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic import DetailView, ListView

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer

from apps.profiles.views import TeamListView, TeamDetailView, StandingsView
from apps.tournaments.views import TournamentDetailView, MatchDetailView, MatchListView, MatchReportView, MatchReportListView, SubmitLineupView, LineupView
from apps.tournaments.models import Match

handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r'^report_match/$', MatchReportListView.as_view(), name="report_match_list"),
    url(r'^report_match/(?P<pk>[\d]+)/$', MatchReportView.as_view(), name="report_match"),
    url(r'^submit_lineup/', SubmitLineupView.as_view(), name="submit_lineup"),
    url(r'^view_lineup/', LineupView.as_view(), name="view_lineup"),
    url(r'^(?P<slug>[\w_-]+)/$', TournamentDetailView.as_view(), name='tournament'),
    url(r'^(?P<tournament>[\w_-]+)/teams/$', TeamListView.as_view(), name='teams'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<slug>[\w_-]+)/$', TeamDetailView.as_view(), name='team_page'),
    url(r'^(?P<tournament>[\w_-]+)/matches/$', MatchListView.as_view(), name='matches'),
    url(r'^matches/(?P<pk>[\d]+)/$', DetailView.as_view(model=Match), name='match_page'),
    #url(r'^(?P<tournament>[\w_-]+)/matches/(?P<date>[\d\\-]+)/(?P<home>[\w_-]+)-vs-(?P<away>[\w_-]+)$', MatchDetailView.as_view(), name='match_page'),
    url(r'^(?P<tournament>[\w_-]+)/standings/$', StandingsView.as_view(), name='standings'),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
