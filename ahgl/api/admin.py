from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.db import transaction
from django.db.models.fields.related import RelatedField
from django.contrib.admin.actions import delete_selected
from django.utils import timezone

from .models import Game, CarouselItem
from profiles.models import Team, TeamMembership

import settings

class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CarouselItemAdmin(admin.ModelAdmin):
	list_display = ('image_url',)

admin.site.register(Game, GameAdmin)
admin.site.register(CarouselItem, CarouselItemAdmin)
