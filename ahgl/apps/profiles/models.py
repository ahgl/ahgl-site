from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase
from imagekit.models import ImageSpec, ProcessedImageField
from imagekit.processors import resize
from imagekit.processors import AutoConvert
import apps.tournaments.models

RACES = (
         ("T", "Terran"),
         ("P", "Protoss"),
         ("Z", "Zerg"),
         ("R", "Random"),
         )

class Profile(ProfileBase):
    name = models.CharField(_("name"), max_length=50)
    photo = ProcessedImageField([resize.Fit(width=352, height=450)], options={'quality': 90}, upload_to='profile_photos', null=True, blank=True)
    custom_thumb = ProcessedImageField([resize.Fit(width=150, height=170)], options={'quality': 90}, upload_to='profile_customthumb_photos', null=True, blank=True)
    _auto_thumbnail = ImageSpec([resize.Fit(width=150, height=170)], image_field='photo', options={'quality': 90}, pre_cache=True)
    #about = models.TextField(_("about"), null=True, blank=True)
    #location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    website = models.URLField(_("website"), null=True, blank=True, verify_exists=False)
    questions_answers = models.TextField(blank=True)
    # photo

    #starcraft data
    char_name = models.CharField(max_length=20, blank=True)
    char_code = models.PositiveSmallIntegerField(null=True, blank=True)
    bnet_profile = models.URLField(null=True, blank=True)
    race = models.CharField(max_length=1, choices=RACES, null=True, blank=True)

    #company data
    title = models.CharField(max_length=70, blank=True)
    
    @property
    def thumbnail(self):
        if self.custom_thumb is not None:
            return self.custom_thumb
        else:
            return self._auto_thumbnail
    
    def is_active(self):
        return self.teams.filter(tournament__active=True).count() > 0
    
    def is_captain(self):
        return self.captain_of.filter(tournament__active=True).count() > 0
    
    def __unicode__(self):
        return self.char_name or self.name


class Team(models.Model):
    """Per Tournament"""
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)
    photo = ProcessedImageField([resize.Fit(width=920, height=450)], options={'quality': 90}, upload_to='team_photos', null=True, blank=True)
    thumbnail = ImageSpec([resize.Fit(width=214, height=120)], image_field='photo', options={'quality': 90}, pre_cache=True)
    charity = models.CharField(max_length=50)
    motto = models.CharField(max_length=70)
    members = models.ManyToManyField('Profile', null=True, blank=True, related_name='teams')
    tournament = models.ForeignKey('tournaments.Tournament', related_name='teams')
    captain = models.ForeignKey('Profile', null=True, blank=True, related_name='captain_of')


    #computed
    rank = models.IntegerField()
    
    @property
    def wins(self):
        return 0
    @property
    def losses(self):
        return 0
    @property
    def tiebreaker(self):
        return 0
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        unique_together = (('name','tournament'),)
