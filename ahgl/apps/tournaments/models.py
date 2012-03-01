import posixpath
import logging
import random
from itertools import chain
import datetime

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

from .tasks import notify_match_creation

logger = logging.getLogger(__name__)

def validate_wholenumber(value):
    if value < 1:
        raise ValidationError(u'{0} is not a whole number'.format(value))

class Tournament(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)
    map_pool = models.ManyToManyField('Map')
    active = models.BooleanField(default=False)
    featured_game = models.ForeignKey('Game', blank=True, null=True, on_delete=models.SET_NULL)
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
    teams = models.ManyToManyField('profiles.Team', related_name='rounds', through='TeamRoundMembership')
    stage = models.IntegerField()
    structure = models.CharField(max_length=1, choices=(('G', 'Group'),('E', 'Elimination'),), default='G')
    
    def participants(self):
        if self.structure=="G":
            return self.team_membership.order_by('-wins', '-tiebreaker').select_related('team')
        else:
            return self.team_membership.order_by('team__seed').select_related('team')
    
    def __unicode__(self):
        return " : ".join((self.name, unicode(self.stage)))
    
    class Meta:
        ordering = ('-stage','name',)

class TeamRoundMembership(models.Model):
    tournamentround = models.ForeignKey('TournamentRound', db_index=True, related_name='team_membership')
    team = models.ForeignKey('profiles.Team', db_index=True, related_name='round_membership')
    wins = models.IntegerField(default=0, editable=False)
    losses = models.IntegerField(default=0, editable=False)
    tiebreaker = models.IntegerField(default=0, editable=False)
    
    def update_stats(self):
        self.wins = self.team.match_wins.filter(published=True, tournament_round=self.tournamentround).count()
        self.losses = self.team.match_losses.filter(published=True, tournament_round=self.tournamentround).count()
        self.tiebreaker = self.team.game_wins.filter(match__published=True, match__tournament_round=self.tournamentround).count() \
                        - self.team.game_losses.filter(match__published=True, match__tournament_round=self.tournamentround).count()
        self.save()

    class Meta:
        db_table = 'tournaments_tournamentround_teams'
        unique_together = (('tournamentround', 'team'),)
        auto_created = True # LOL, this is a terrible hack that keeps add and remove around; only use this if all fields are auto

class Match(models.Model):
    home_team = models.ForeignKey('profiles.Team', related_name="home_matches")
    away_team = models.ForeignKey('profiles.Team', related_name="away_matches")
    tournament = models.ForeignKey('Tournament', related_name='matches')
    tournament_round = models.ForeignKey('TournamentRound', related_name='matches')
    published = models.BooleanField(default=False)
    publish_date = models.DateField(blank=True, null=True) #set this when published
    creation_date = models.DateField()
    referee = models.ForeignKey('profiles.Profile', null=True, blank=True, editable=False)
    # submitted lineups yet?
    home_submitted = models.BooleanField(default=False)
    away_submitted = models.BooleanField(default=False)
    winner = models.ForeignKey('profiles.Team', related_name="match_wins", blank=True, null=True, editable=False)
    loser = models.ForeignKey('profiles.Team', related_name="match_losses", blank=True, null=True, editable=False)    
    
    def update_winloss(self):
        for team in (self.home_team, self.away_team):
            team.wins = team.match_wins.filter(published=True).count()
            team.losses = team.match_losses.filter(published=True).count()
            team.save()
            try:
                membership = TeamRoundMembership.objects.get(team=team, tournamentround=self.tournament_round)
            except TeamRoundMembership.DoesNotExist:
                pass
            else:
                membership.wins = team.match_wins.filter(published=True, tournament_round=self.tournament_round).count()
                membership.losses = team.match_losses.filter(published=True, tournament_round=self.tournament_round).count()
                membership.save()

    def update_tiebreaker(self):        
        for team in (self.home_team, self.away_team):
            team.tiebreaker = team.game_wins.filter(match__published=True).count() - team.game_losses.filter(match__published=True).count()
            team.save()
            try:
                membership = TeamRoundMembership.objects.get(team=team, tournamentround=self.tournament_round)
            except TeamRoundMembership.DoesNotExist:
                pass
            else:
                membership.tiebreaker = team.game_wins.filter(match__published=True, match__tournament_round=self.tournament_round).count() \
                                        - team.game_losses.filter(match__published=True, match__tournament_round=self.tournament_round).count()
                membership.save()

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
    
    def remove_extra_victories(self):
        """only count the games that matter to win and set the others to have no winner"""
        games = list(self.games.all())
        home_wins, away_wins = 0, 0
        win_point = (len(games)//2)+1
        for game in games:
            # if someone already has the games to win (not counting this one) - this game does not matter
            if (home_wins >= win_point or away_wins >= win_point) and game.winner:
                game.winner = None
                game.full_clean()
                game.save()
            if game.winner_team == self.home_team:
                home_wins += 1
            else:
                away_wins += 1
            
    def save(self, notify=True, *args, **kwargs):
        created = self.id is None
        if created and not self.creation_date: # set creation date if it wasn't set already
            self.creation_date = datetime.datetime.now()
        super(Match, self).save(*args, **kwargs)
        if "notification" in settings.INSTALLED_APPS and notification and created and notify:
            notify_match_creation.delay(unicode(self),
                                        self.home_team.pk,
                                        self.away_team.pk,
                                        getattr(self.home_team.captain, "pk", None),
                                        getattr(self.away_team.captain, "pk", None)
                                        )

    def games_with_map(self):
        return self.games.select_related('map')
    def games_with_related(self):
        return self.games.select_related('map', 'home_player__user', 'away_player__user')
    def games_played(self):
        return self.games.select_related('map', 'home_player__user', 'away_player__user', 'winner').exclude(winner__isnull=True)
    
    def first_vod(self):
        try:
            return self.games_played()[0].vod
        except IndexError:
            return None
    
    def __unicode__(self):
        return u" ".join((u" vs ".join((unicode(self.home_team), unicode(self.away_team))), str(self.creation_date)))
    
    @models.permalink
    def get_absolute_url(self, tournament_slug=None):
        if not tournament_slug:
            tournament_slug = self.tournament.slug
        return ('match_page', (), {'tournament': tournament_slug,
                                  'pk': self.pk,
                                  }
                )
    
def replay_path(instance, filename):
    match = instance.match
    tournament = match.tournament
    filename = "_".join((unicode(instance.home_player), unicode(instance.away_player), unicode(instance.map), u".SC2Replay")).encode('ascii', 'ignore')
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
        else:
            self.loser = None
            self.winner_team = None
            self.loser_team = None
        
    # computes match wins
    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)
        total_games = self.match.games.count()
        hwins = len([g for g in self.match.games.all() if g.home_player==g.winner])
        awins = len([g for g in self.match.games.all() if g.away_player==g.winner])
        if hwins > (total_games // 2):
            if self.match.winner != self.match.home_team:
                self.match.winner = self.match.home_team
                self.match.full_clean()
                self.match.save()
        elif awins > (total_games // 2):
            if self.match.winner != self.match.away_team:
                self.match.winner = self.match.away_team
                self.match.full_clean()
                self.match.save()
        else:
            if self.winner:
                self.match.winner = None
                self.match.full_clean()
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

@receiver(post_save, sender=Match, dispatch_uid="tournaments_update_winloss")
def update_winloss(sender, instance, created, **kwargs):
    if instance.published and instance.winner:
        instance.update_winloss()            
    
@receiver(post_save, sender=Game, dispatch_uid="tournaments_update_tiebreaker")
def update_tiebreaker(sender, instance, created, **kwargs):
    instance.match.update_tiebreaker()
