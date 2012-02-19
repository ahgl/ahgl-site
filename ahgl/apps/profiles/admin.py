from django.contrib import admin

from .models import Profile, Team, Charity

class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'tournament','seed',)
    list_filter = ('tournament',)
    ordering = ('tournament',)
    list_editable = ('seed',)
   
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'char_name',)
    list_filter = ('teams',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Charity)