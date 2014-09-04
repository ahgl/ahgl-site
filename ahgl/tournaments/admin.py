from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.db import transaction
from django.db.models.fields.related import RelatedField
from django.contrib.admin.actions import delete_selected
from django.utils import timezone

from .views import NewTournamentRoundView
from .models import Article, Tournament, TournamentRound, Map, Match, Game
from profiles.models import Team, TeamMembership

from .tasks import update_round_stats
import settings


class TournamentRoundInline(admin.TabularInline):
    model = TournamentRound

    def get_formset(self, request, obj=None, **kwargs):
        self.parent = obj
        return super(TournamentRoundInline, self).get_formset(request, obj=obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "teams":
            queryset = Team.objects.filter(tournament=self.parent) if self.parent else Team.objects.all()
            request.team_queryset = kwargs["queryset"] = queryset.only('name')
        return super(TournamentRoundInline, self).formfield_for_manytomany(db_field, request, **kwargs)


class TournamentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'status',)
    list_filter = ('status',)
    inlines = (TournamentRoundInline,)

    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj
        return super(TournamentAdmin, self).get_form(request, obj, **kwargs)

    @transaction.commit_manually
    def save_model(self, request, obj, form, change):
        try:
            super(TournamentAdmin, self).save_model(request, obj, form, change)
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()
            update_round_stats.delay(obj.pk)
            if getattr(settings, "CELERY_ALWAYS_EAGER", False) is True:
                transaction.commit()  # must commit if running in eager task mode

    def get_urls(self):
        urls = super(TournamentAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'(?P<tournament>[\w_-]+)/new_round/?((?P<stage>[\d]+)/)?$', self.admin_site.admin_view(NewTournamentRoundView.as_view()), name="new_round"),
        )
        return my_urls + urls


class GameInline(admin.TabularInline):
    model = Game
    extra = 1

    team_field_removals = set(('home_player', 'away_player', 'home_race', 'away_race', 'winner', 'replay',))
    individual_field_removals = set(('winner_team',))

    def get_formset(self, request, obj=None, **kwargs):
        self.parent = obj
        if obj:
            if obj.structure == "I":
                self.exclude = self.individual_field_removals
            elif obj.structure == "T":
                self.exclude = self.team_field_removals
        return super(GameInline, self).get_formset(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if "player" in db_field.name or db_field.name == "winner":
            if hasattr(request, "membership_queryset"):
                kwargs["queryset"] = request.membership_queryset
            else:
                request.membership_queryset = kwargs["queryset"] = TeamMembership.objects.filter(team__in=[self.parent.home_team, self.parent.away_team]).only('char_name')
        cache_field("team", Team.objects.filter(tournament=self.parent.tournament_id) if self.parent else Team.objects.all(), db_field, request, kwargs)
        cache_field("map", self.parent.tournament.map_pool.all() if self.parent else Map.objects.all(), db_field, request, kwargs)
        return super(GameInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        queryset = super(GameInline, self).queryset(request) \
                                          .select_related('home_player', 'away_player')
        if request.method.lower() == "GET":
            only = ['home_player__char_name', 'away_player__char_name', 'map', 'winner', 'winner_team']
            only += [field.name for field in self.model._meta.fields if field.editable and not isinstance(field, RelatedField)]
            queryset = queryset.only(*only)
        return queryset


def cache_field(field_name, queryset, db_field, request, kwargs):
    attr = "_".join((field_name, "queryset"))
    if field_name in db_field.name:
        if not hasattr(request, attr):
            setattr(request, attr, queryset)
        kwargs['queryset'] = getattr(request, attr)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'winner__name', 'creation_date', 'publish_date', 'home_submission_date', 'away_submission_date', 'tournament_round', 'published',)
    list_filter = ('tournament', 'home_submitted', 'away_submitted',)
    search_fields = ('home_team__name', 'away_team__name',)
    inlines = (GameInline,)
    actions = ['publish_match', 'delete_and_update_stats']
    date_hierarchy = 'creation_date'
    readonly_fields = ('tournament', 'home_submission_date', 'away_submission_date', 'referee',)

    def has_add_permission(self, request):
        return False

    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj
        return super(MatchAdmin, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        cache_field("team", Team.objects.filter(tournament=self.obj.tournament_id), db_field, request, kwargs)
        cache_field("tournament_round", TournamentRound.objects.filter(tournament=self.obj.tournament_id).only('order', 'stage_name'), db_field, request, kwargs)
        return super(MatchAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        queryset = super(MatchAdmin, self).queryset(request).select_related('tournament', 'home_team', 'away_team', 'winner').prefetch_related('tournament_round') \
                                          .defer('tournament__status', 'tournament__games_per_match')
        return queryset

    def publish_match(self, request, queryset):
        rows_updated = queryset.update(published=True, publish_date=timezone.now())
        for match in queryset.all():
            match.update_winloss()
            match.update_tiebreaker()
        if rows_updated == 1:
            message_bit = "1 match was"
        else:
            message_bit = "%s match were" % rows_updated
        self.message_user(request, "%s successfully published." % message_bit)
    publish_match.short_description = "Publish matches so they are visible to all users"

    def delete_and_update_stats(self, request, queryset):
        ret = delete_selected(self, request, queryset)
        if request.POST.get('post'):
            teamset = set()
            for match in queryset:
                for team in (match.home_team, match.away_team):
                    if team:
                        teamset.add(team)
            for team in teamset:
                team.update_stats()
        return ret
    delete_and_update_stats.short_description = "Deletes matches and updates all team stats associated with those matches"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'publish_date', 'published',)
    fields = ('title', 'summary', 'published', 'tournaments')

    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj
        return super(ArticleAdmin, self).get_form(request, obj, **kwargs)

    @transaction.commit_manually
    def save_model(self, request, obj, form, change):
        try:
            super(ArticleAdmin, self).save_model(request, obj, form, change)
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Map)
admin.site.register(Match, MatchAdmin)
admin.site.register(Article, ArticleAdmin)
