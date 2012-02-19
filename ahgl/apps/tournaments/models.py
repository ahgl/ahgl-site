import posixpath
import logging
import random

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.exceptions import ValidationError

if "sorl.thumbnail" in settings.INSTALLED_APPS:
    from sorl.thumbnail import ImageField
else:
    from django.db.models import ImageField
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

from apps.profiles import RACES

logger = logging.getLogger(__name__)

def validate_wholenumber(value):
    if value < 1:
        raise ValidationError(u'{0} is not a whole number'.format(value))

class Tournament(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)
    map_pool = models.ManyToManyField('Map')
    active = models.BooleanField(default=False)
    featured_game = models.ForeignKey('Game', blank=True, null=True)
    games_per_match = models.PositiveSmallIntegerField(default=5, verbose_name="Default Games per Match", validators=[validate_wholenumber])
    
    def random_teams(self, amount=7):
        return self.teams.order_by('?')[:amount]
    
    def stages(self):
        return [row['stage'] for row in self.rounds.values('stage').distinct().order_by('stage')]
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('tournament', (), {'slug': self.slug,
                                   }
                )

class Map(models.Model):
    name = models.CharField(_("name"), max_length=50, primary_key=True)
    photo = ImageField(upload_to='map_photos', null=True, blank=True)
    # TODO:maybe add computed statistics later?
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
    
class TournamentRound(models.Model):
    name = models.CharField(max_length=40)
    tournament = models.ForeignKey('Tournament', related_name='rounds')
    teams = models.ManyToManyField('profiles.Team', related_name='rounds')
    stage = models.IntegerField()
    structure = models.CharField(max_length=1, choices=(('G', 'Group'),('E', 'Elimination'),), default='G')
    
    def participants(self):
        if self.structure=="G":
            return self.teams.order_by('-tiebreaker', '-wins')
        else:
            return self.teams.order_by('seed')
    
    class Meta:
        ordering = ('stage','name',)

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
    winner = models.ForeignKey('profiles.Team', related_name="match_wins", blank=True, null=True, editable=False)
    loser = models.ForeignKey('profiles.Team', related_name="match_losses", blank=True, null=True, editable=False)    
    
    # validates winner is one of the teams and sets the loser to the other team
    def clean(self):
        super(Match, self).clean()
        from django.core.exceptions import ValidationError
        if self.winner:
            if self.winner == self.home_team:
                self.loser = self.away_team
            elif self.winner == self.away_team:
                self.loser = self.home_team
            else:
                raise ValidationError("Winner must be one of the teams playing")
            
    def save(self, *args, **kwargs):
        created = self.id is None
        super(Match, self).save(*args, **kwargs)
        if notification and created:
            notification.send(User.objects.filter(profile__teams__pk__in=(self.home_team.pk, self.away_team.pk)),
                      "tournaments_new_match",
                      {'match': self,
                       })

    def games_played(self):
        return self.games.exclude(winner__isnull=True)
    
    def first_vod(self):
        try:
            return self.games.exclude(vod__isnull=True)[0].vod
        except IndexError:
            return None
    
    def __unicode__(self):
        return u" ".join((u" vs ".join((unicode(self.home_team), unicode(self.away_team))), str(self.creation_date)))
    
    @models.permalink
    def get_absolute_url(self):
        return ('match_page', (), {'pk': self.pk,
                                   }
                )
    
def replay_path(instance, filename):
    match = instance.match
    tournament = match.tournament
    filename = "_".join((unicode(instance.home_player), unicode(instance.away_player), unicode(instance.map), u".SC2Replay"))
    return posixpath.join("replays", unicode(tournament), unicode(match), filename)
class Game(models.Model):
    match = models.ForeignKey('Match', related_name="games")
    map = models.ForeignKey('Map') #add verification that this is in map pool for tournament
    order = models.PositiveSmallIntegerField()
    home_player = models.ForeignKey('profiles.Profile', related_name="home_games", null=True, blank=True, on_delete=models.SET_NULL)
    home_race = models.CharField(max_length=1, choices=RACES, blank=True) #TODO: default to player's race in UI
    away_player = models.ForeignKey('profiles.Profile', related_name="away_games", null=True, blank=True, on_delete=models.SET_NULL)
    away_race = models.CharField(max_length=1, choices=RACES, blank=True) #TODO: default to player's race in UI
    winner = models.ForeignKey('profiles.Profile', related_name="game_wins", blank=True, null=True, on_delete=models.SET_NULL)
    loser = models.ForeignKey('profiles.Profile', related_name="game_losses", blank=True, null=True, editable=False, on_delete=models.SET_NULL)
    winner_team = models.ForeignKey('profiles.Team', related_name="game_wins", blank=True, null=True, editable=False)
    loser_team = models.ForeignKey('profiles.Team', related_name="game_losses", blank=True, null=True, editable=False)
    forfeit = models.BooleanField(default=False)
    replay = models.FileField(upload_to=replay_path, max_length=300, null=True, blank=True)
    vod = models.URLField(null=True, blank=True)
    is_ace = models.BooleanField(default=False)
    
    # validate winner is one of the players and sets the loser to the other player
    # also set the winner and loser team
    def clean(self):
        super(Game, self).clean()
        from django.core.exceptions import ValidationError
        if self.winner:
            if self.winner == self.home_player:
                self.loser = self.away_player
                self.winner_team = self.match.home_team
                self.loser_team = self.match.away_team
            elif self.winner == self.away_player:
                self.loser = self.home_player
                self.winner_team = self.match.away_team
                self.loser_team = self.match.home_team
            else:
                raise ValidationError("Winner must be one of the players playing")
        
    # computes match wins
    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)
        total_games = self.match.games.count()
        hwins = self.match.games.filter(winner=self.home_player).count()
        awins = self.match.games.filter(winner=self.away_player).count()
        if hwins > (total_games // 2) and self.match.winner != self.match.home_team:
            self.match.winner = self.match.home_team
            self.match.clean()
            self.match.save()
        elif awins > (total_games // 2) and self.match.winner != self.match.away_team:
            self.match.winner = self.match.away_team
            self.match.clean()
            self.match.save()
            
    def __unicode__(self):
        if self.home_player and self.away_player:
            ret = u" vs ".join((unicode(self.home_player), unicode(self.away_player)))
        else:
            ret = unicode(self.match)
        return u" on ".join((ret, unicode(self.map)))
        
    class Meta:
        unique_together = (('order','match'),)
        ordering = ('order',)
