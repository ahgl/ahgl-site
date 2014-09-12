from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from tinymce.widgets import TinyMCE
from phileo.models import Like

from .models import Profile, Team, Charity, TeamMembership, Caster
from .fields import HTMLField


class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'tournament', 'seed', 'status', 'paid', 'charity',)
    list_filter = ('tournament', 'status', 'charity', 'paid',)
    ordering = ('tournament',)
    list_editable = ('seed', 'paid',)


class TeamMembershipAdminInline(admin.TabularInline):
    model = TeamMembership
    extra = 1
    exclude = ('questions_answers',)
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(mce_attrs={'theme': 'advanced'})},
    }


class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'active', 'captain',)
    list_filter = ('team', 'race', 'champion', 'captain',)
    search_fields = ('char_name',)
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(mce_attrs={'theme': 'advanced'})},
    }

class AwaitingTeamMembership(TeamMembership):
    class Meta:
        proxy = True

class AwaitingTeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('profile', 'team', 'active', 'status',)
    list_filter = ('team', 'race', 'champion', 'captain',)
    actions = ['approve', 'reject']
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(mce_attrs={'theme': 'advanced'})},
    }

    def queryset(self, request):
        return self.model.objects.filter(status='W')

    def approve(self, request, queryset):
        rows_updated = queryset.update(status='A')
        if rows_updated == 1:
            message_bit = "1 match was"
        else:
            message_bit = "%s match were" % rows_updated
        self.message_user(request, "%s successfully approved." % message_bit)
    approve.short_description = "Approve awaiting requests"

    def reject(self, request, queryset):
        rows_updated = queryset.update(status='R')
        if rows_updated == 1:
            message_bit = "1 membership was"
        else:
            message_bit = "%s membership were" % rows_updated
        self.message_user(request, "%s successfully rejected." % message_bit)
    reject.short_description = "Reject awaiting requests"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )
    list_filter = ('teams',)
    search_fields = ('name', 'team_membership__char_name', 'user__username',)
    inlines = (TeamMembershipAdminInline,)


class CasterAdmin(admin.ModelAdmin):
    list_display = ('user', )
    actions = ['reset_votes']

    def reset_votes(self, request, queryset):
        for caster in queryset.all():
            Like.objects.filter(
                receiver_content_type=ContentType.objects.get_for_model(caster),
                receiver_object_id=caster.pk).delete()
        # Commented out because `rows_deleted` doesn't exist.
        # self.message_user(request, "Votes successfully deleted.".format(rows_deleted))

admin.site.register(TeamMembership, TeamMembershipAdmin)
admin.site.register(AwaitingTeamMembership, AwaitingTeamMembershipAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Charity)
admin.site.register(Caster, CasterAdmin)
