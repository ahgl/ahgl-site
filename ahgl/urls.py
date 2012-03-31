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
from apps.profiles.views import TeamListView, TeamDetailView, StandingsView, TeamUpdateView, MyProfileDetailView, TeamMembershipView, TeamMembershipUpdateView
from apps.tournaments.views import MatchDetailView, MatchListView, MatchReportView, SubmitLineupView, GameListView, PlayerAdminView
from apps.tournaments.models import Match, Tournament

handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r'^social/', include('social_auth.urls')),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/profile/(?P<slug>[\w\._-]+)/$", MyProfileDetailView.as_view(), name="profile_detail"),
    url(r"^profiles/edit/$", ProfileUpdateView.as_view(form_class=model_forms.modelform_factory(Profile, exclude=('user','signature','signature_html','time_zone','language','post_count','avatar',))), name="profile_edit"),
    url(r"^profiles/membership_edit/(?P<pk>[\d]+)/$", TeamMembershipUpdateView.as_view(), name="membership_edit"),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^messages/compose/(?P<recipient>[\+\w\.\-_]+)/$', compose, name='messages_compose_to'), #we allow periods
    url(r'^messages/', include('messages.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    
    # player admin controls
    url(r'^player_admin/$', PlayerAdminView.as_view(), name="player_admin"),
    url(r'^report_match/(?P<pk>[\d]+)/$', MatchReportView.as_view(), name="report_match"),
    # captain specific
    url(r'^submit_lineup/(?P<pk>[\d]+)/$', SubmitLineupView.as_view(), name="submit_lineup"),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<slug>[\w_-]+)/edit/$', TeamUpdateView.as_view(), name='edit_team'),
    
    url(r'^archive/$', ListView.as_view(queryset=Tournament.objects.filter(active=False), template_name="tournaments/archives.html"), name="archives"),
    url(r'^games/$', GameListView.as_view(), name='games'),
    url(r'^(?P<tournament>[\w_-]+)/games/$', GameListView.as_view(), name='games'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<team>[\w_-]+)/(?P<profile>[\w\._-]+)/games/$', GameListView.as_view(), name='games'),
    url(r'^(?P<tournament>[\w_-]+)/teams/$', TeamListView.as_view(), name='teams'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<slug>[\w_-]+)/$', TeamDetailView.as_view(), name='team_page'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<team>[\w_-]+)/(?P<profile>[\w\._-]+)/$', TeamMembershipView.as_view(), name='player_profile'),
    url(r'^(?P<tournament>[\w_-]+)/schedule/$', MatchListView.as_view(template_name="tournaments/schedule.html"), name='schedule'),
    url(r'^(?P<tournament>[\w_-]+)/matches/$', MatchListView.as_view(), name='matches'),
    url(r'^(?P<tournament>[\w_-]+)/matches/(?P<pk>[\d]+)/$', MatchDetailView.as_view(), name='match_page'),
    #url(r'^(?P<tournament>[\w_-]+)/matches/(?P<date>[\d\\-]+)/(?P<home>[\w_-]+)-vs-(?P<away>[\w_-]+)$', MatchDetailView.as_view(), name='match_page'),
    url(r'^(?P<tournament>[\w_-]+)/standings/$', StandingsView.as_view(), name='standings'),
    url(r'^', include('cms.urls')),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)