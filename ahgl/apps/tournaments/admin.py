from django.utils.functional import curry
from django.contrib import admin
from django import forms
from django.conf.urls.defaults import patterns, url

from .views import NewTournamentRoundView
from .models import Tournament, TournamentRound, Map, Match, Game
from apps.profiles.models import Team, Game

class TournamentRoundInline(admin.TabularInline):
    model = TournamentRound
    
    def get_formset(self, request, obj=None, **kwargs):
        self.parent = obj
        return super(TournamentRoundInline, self).get_formset(request, obj=obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "teams":
            if self.parent:
                kwargs["queryset"] = Team.objects.filter(tournament=self.parent)
        return super(TournamentRoundInline, self).formfield_for_manytomany(db_field, request, **kwargs)


class TournamentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'active',)
    list_filter = ('active',)
    inlines = [
        TournamentRoundInline,
    ]
    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj
        return super(TournamentAdmin, self).get_form(request, obj, **kwargs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "featured_game":
            kwargs["queryset"] = Game.objects.filter(match__published=True, match__tournament=self.obj).order_by('match__publish_date')
        return super(TournamentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_urls(self):
        urls = super(TournamentAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'(?P<tournament>[\w_-]+)/new_round/?((?P<stage>[\d]+)/)?$', self.admin_site.admin_view(NewTournamentRoundView.as_view()), name="new_round"),
        )
        return my_urls + urls

class GameInline(admin.TabularInline):
    model = Game


class MatchAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'tournament', 'home_team','away_team', 'published',)
    list_filter = ('tournament',)
    search_fields = ('home_team__name','away_team__name',)
    inlines = [
        GameInline,
    ]
    actions = ['publish_match']
    
    def publish_match(self, request, queryset):
        rows_updated = queryset.update(published=True)
        if rows_updated == 1:
            message_bit = "1 match was"
        else:
            message_bit = "%s match were" % rows_updated
        self.message_user(request, "%s successfully published." % message_bit)
    publish_match.short_description = "Publish matches so they are visible to all users"

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Map)
admin.site.register(Match, MatchAdmin)
