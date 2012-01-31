import posixpath

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.profiles.models import RACES

GAME_OUTCOME = (
                ("H", "Home"),
                ("A", "Away"),
                ("N", "Not played"),
                )

class Tournament(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)
    map_pool = models.ManyToManyField('Map')
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Map(models.Model):
    name = models.CharField(_("name"), max_length=50, primary_key=True)
    # maybe add computed statistics later?
    def __unicode__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey('profiles.Team', related_name="home_matches")
    away_team = models.ForeignKey('profiles.Team', related_name="away_matches")
    tournament = models.ForeignKey('Tournament', related_name='matches')
    published = models.BooleanField(default=False)
    publish_date = models.DateField(blank=True, null=True) #set this when published
    creation_date = models.DateField(auto_now_add=True)
    referee = models.ForeignKey('profiles.Profile', null=True, blank=True, editable=False)
    # submitted lineups yet?
    home_submitted = models.BooleanField(default=False)
    away_submitted = models.BooleanField(default=False)
    
    def games_in_order(self):
        return self.games.order_by('order')
    
    def games_played(self):
        return self.games.exclude(winner="N").order_by('order')
    
    def __unicode__(self):
        return u" ".join((u" vs ".join((self.home_team.name, self.away_team.name)), str(self.creation_date)))
    
def replay_path(instance, filename):
    match = instance.match
    tournament = match.tournament
    filename = "_".join((unicode(instance.home_player), unicode(instance.away_player), unicode(instance.map), u".SC2Replay"))
    return posixpath.join("replays", unicode(tournament), unicode(match), filename)
class Game(models.Model):
    match = models.ForeignKey('Match', related_name="games")
    map = models.ForeignKey('Map') #add verification that this is in map pool for tournament
    order = models.PositiveSmallIntegerField()
    home_player = models.ForeignKey('profiles.Profile', related_name="home_games", null=True, blank=True)
    home_race = models.CharField(max_length=1, choices=RACES, blank=True) #TODO: default to player's race in UI
    away_player = models.ForeignKey('profiles.Profile', related_name="away_games", null=True, blank=True)
    away_race = models.CharField(max_length=1, choices=RACES, blank=True) #TODO: default to player's race in UI
    winner = models.CharField(max_length=1, choices=GAME_OUTCOME, blank=True) #blank means hasn't been played yet
    forfeit = models.BooleanField(default=False)
    replay = models.FileField(upload_to=replay_path, null=True, blank=True)
    vod = models.URLField(null=True, blank=True)
    is_ace = models.BooleanField(default=False)
        
    class Meta:
        unique_together = (('order','match'),)

    
    
    