from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.views.generic import ListView
from django.conf.urls.static import static
from django.forms import models as model_forms

from django.contrib import admin
admin.autodiscover()

from idios.views import ProfileUpdateView
from django_messages.views import compose

from profiles.models import Profile
from profiles.views import (MVPView, TeamListView, TeamDetailView, TeamAdminView,
                            StandingsView, TeamUpdateView, TeamSignupView,
                            MyProfileDetailView, TeamMembershipView,
                            TeamMembershipUpdateView, TeamMembershipCreateView,
                            TeamMembershipDeleteView, CasterListView,
                            JoinTeamView)
from tournaments.views import (MatchDetailView, MatchListView, MatchReportView,
                               SubmitLineupView, GameListView, PlayerAdminView)
from tournaments.models import Tournament


from django.conf.urls import patterns, url, include
from rest_framework import routers
from ahgl.api.views import header, games, matches, carousel

router = routers.DefaultRouter()
router.register(r'header', header.HeaderViewSet)
router.register(r'games', games.GamesViewSet)
router.register(r'featured_matches', matches.FeaturedMatchesViewSet)
router.register(r'carousel', carousel.CarouselItemViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
)

urlpatterns += patterns('',
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("recaptcha_form.account_backend.urls")),
    url(r'^social/', include('social_auth.urls')),
    url(r"^profiles/profile/(?P<slug>[\w\._-]+)/$", MyProfileDetailView.as_view(), name="profile_detail"),
    url(r"^profiles/profile/(?P<slug>[\w\._-]+)/add_membership/$", TeamMembershipCreateView.as_view(), name="membership_create"),
    url(r"^profiles/edit/$", ProfileUpdateView.as_view(form_class=model_forms.modelform_factory(Profile, exclude=('user', 'signature', 'signature_html', 'time_zone', 'language', 'post_count', 'avatar',))), name="profile_edit"),
    url(r"^profiles/membership_edit/(?P<pk>[\d]+)/$", TeamMembershipUpdateView.as_view(), name="membership_edit"),
    url(r"^profiles/membership_delete/(?P<pk>[\d]+)/$", TeamMembershipDeleteView.as_view(), name="membership_delete"),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^likes/", include("phileo.urls")),
    url(r"^announcements/", include("announcements.urls")),
    # url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^messages/compose/(?P<recipient>[\+\w\.\-_]+)/$', compose, name='messages_compose_to'),  # we allow periods
    url(r'^messages/', include('django_messages.urls')),
    url(r'^tinymce/', include('tinymce.urls')),

    # player admin controls
    url(r'^player_admin/$', PlayerAdminView.as_view(), name="player_admin"),
    url(r'^report_match/(?P<pk>[\d]+)/$', MatchReportView.as_view(), name="report_match"),
    # captain specific
    url(r'^submit_lineup/(?P<pk>[\d]+)/$', SubmitLineupView.as_view(), name="submit_lineup"),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<slug>[\w_-]+)/edit/$', TeamUpdateView.as_view(), name='edit_team'),

    url(r'^archive/$', ListView.as_view(queryset=Tournament.objects.filter(status='C'), template_name="tournaments/archives.html"), name="archives"),
    url(r'^games/$', GameListView.as_view(), name='games'),
    url(r'^team/signup/$', TeamSignupView.as_view(), name='signup_team'),
    url(r'^team_admin/$', TeamAdminView.as_view(), name="team_admin"),
    url(r'^(?P<tournament>[\w_-]+)/mvp/$', MVPView.as_view(), name='mvp'),
    url(r'^(?P<tournament>[\w_-]+)/videos/$', GameListView.as_view(template_name="tournaments/videos.html", vod_only=True), name='videos'),
    url(r'^(?P<tournament>[\w_-]+)/games/$', GameListView.as_view(), name='games'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<team>[\w_-]+)/(?P<profile>[\w\._-]+)/games/$', GameListView.as_view(), name='games'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<team>[\w_-]+)/matches/$', MatchListView.as_view(template_name="tournaments/team_match_list.html"), name='matches'),
    url(r'^(?P<tournament>[\w_-]+)/teams/$', TeamListView.as_view(), name='teams'),
    #url(r'^(?P<tournament>[\w_-]+)/teams/create/$', TeamCreateView.as_view(), name='create_team'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<slug>[\w_-]+)/$', TeamDetailView.as_view(), name='team_page'),
    url(r'^(?P<tournament>[\w_-]+)/teams/(?P<team>[\w_-]+)/(?P<profile>[\w\._-]+)/$', TeamMembershipView.as_view(), name='player_profile'),
    url(r'^(?P<tournament>[\w_-]+)/schedule/$', MatchListView.as_view(template_name="tournaments/schedule.html"), name='schedule'),
    url(r'^(?P<tournament>[\w_-]+)/matches/$', MatchListView.as_view(), name='matches'),
    url(r'^(?P<tournament>[\w_-]+)/matches/(?P<pk>[\d]+)/$', MatchDetailView.as_view(), name='match_page'),
    #url(r'^(?P<tournament>[\w_-]+)/matches/(?P<date>[\d\\-]+)/(?P<home>[\w_-]+)-vs-(?P<away>[\w_-]+)$', MatchDetailView.as_view(), name='match_page'),
    url(r'^(?P<tournament>[\w_-]+)/standings/$', StandingsView.as_view(), name='standings'),
    url(r'^(?P<tournament>[\w_-]+)/casters/$', CasterListView.as_view(), name='casters'),

    url(r'^join_team/(?P<team>[\w_-]+)/$', JoinTeamView.as_view(), name='join_team'),

    url(r'^', include('cms.urls')),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
