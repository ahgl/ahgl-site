from django.contrib import admin

from profiles.models import Profile, Team

class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Profile)
admin.site.register(Team, TeamAdmin)