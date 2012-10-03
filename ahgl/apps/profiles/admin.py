from django.contrib import admin

from tinymce.widgets import TinyMCE

from .models import Profile, Team, Charity, TeamMembership
from .fields import HTMLField

class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'tournament','seed','status','charity',)
    list_filter = ('tournament','status','charity',)
    ordering = ('tournament',)
    list_editable = ('seed',)
   
class TeamMembershipAdminInline(admin.TabularInline):
    model = TeamMembership
    extra = 1
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(mce_attrs={'theme':'advanced'})},
    }
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'active','captain',)
    list_filter = ('team','race','champion','captain',)
    search_fields = ('char_name',)
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(mce_attrs={'theme':'advanced'})},
    }

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )
    list_filter = ('teams',)
    search_fields = ('name','team_membership__char_name','user__username',)
    inlines = (TeamMembershipAdminInline,)
    


admin.site.register(TeamMembership, TeamMembershipAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Charity)