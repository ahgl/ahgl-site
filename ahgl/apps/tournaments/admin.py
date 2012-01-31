from django.contrib import admin

from tournaments.models import Tournament, Map, Match, Game

class TournamentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class GameInline(admin.TabularInline):
    model = Game

class MatchAdmin(admin.ModelAdmin):
    inlines = [
        GameInline,
    ]
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Map)
admin.site.register(Match, MatchAdmin)
