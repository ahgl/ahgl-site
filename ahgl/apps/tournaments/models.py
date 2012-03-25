from collections import namedtuple
import posixpath
import logging
import random, math
from itertools import chain, count, takewhile
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import date

from cms.models.pluginmodel import CMSPlugin
from celery.execute import send_task
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
    games_per_match = models.PositiveSmallIntegerField(default=5, verbose_name="Default Games per Match", validators=[validate_wholenumber])
    structure = models.CharField(max_length=1, choices=(('I', 'Individual'),('T', 'Team'),), default='I')
    
    def random_teams(self, amount=7):
        return self.teams.order_by('?')[:amount]
    
    def stages(self):
        return self.rounds.values('stage_name', 'stage_order').distinct().order_by('stage_order')
    
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

BracketRow = namedtuple("BracketRow", "items, name")
TeamBracketRecord = namedtuple("TeamBracketRecord", "team_membership, winner")
class TournamentRound(models.Model):
    order = models.IntegerField()
    tournament = models.ForeignKey('Tournament', related_name='rounds')
    teams = models.ManyToManyField('profiles.Team', related_name='rounds', through='TeamRoundMembership')
    stage_order = models.IntegerField()
    stage_name = models.CharField(max_length=40)
    structure = models.CharField(max_length=1, choices=(('G', 'Group'),('E', 'Elimination'),), default='G')
    
    def _round_name(self, count):
        return {1:"Champion", 2:"Finals", 4:"Semi-finals"}.get(count) or "Round of {0}".format(count)
    def elim_bracket(self):
        participants = list(self.participants())
        for wins_needed in takewhile(lambda x:participants, count(1)):
            num_players = len(participants)
            yield BracketRow([TeamBracketRecord(team_membership, team_membership.wins>=wins_needed) for team_membership in participants], self._round_name(num_players))
            participants = [team_membership for team_membership in participants if team_membership.wins>=wins_needed]
        num_players = num_players // 2
        while num_players:
            yield BracketRow([TeamBracketRecord(None, False)]*num_players, self._round_name(num_players))
            num_players = num_players // 2
    
    def participants(self):
        queryset = self.team_membership.select_related('team')
        if self.structure=="G":
            return queryset.order_by('-wins', '-tiebreaker', 'team__seed')
        else:
            return queryset.order_by('team__seed')
    
    def has_matches(self):
        return self.matches.filter(published=True).count()
    
    def __unicode__(self):
        return " : ".join((self.stage_name, unicode(self.order)))
    
    class Meta:
        ordering = ('-stage_order','order',)

class TeamRoundMembership(models.Model):
    tournamentround = models.ForeignKey('TournamentRound', db_index=True, related_name='team_membership')
    team = models.ForeignKey('profiles.Team', db_index=True, related_name='round_membership')
    wins = models.IntegerField(default=0, editable=False)
    losses = models.IntegerField(default=0, editable=False)
    tiebreaker = models.IntegerField(default=0, editable=False)
    #TODO: moving seeding here
    
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
    home_submission_date = models.DateTimeField(blank=True, null=True, editable=False)
    away_submission_date = models.DateTimeField(blank=True, null=True, editable=False)
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
                game.winner_team = None
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
            send_task("tournaments.tasks.notify_match_creation", [unicode(self),
                                                      self.home_team_id,
                                                      self.away_team_id,
                                                      ])

    def games_with_map(self):
        return self.games.select_related('map').only('map__name', 'order', 'is_ace')
    def games_with_related(self):
        if self.home_submitted and self.away_submitted:
            return self.games.select_related('map', 'home_player__team', 'home_player__profile', 'away_player__team', 'away_player__profile') \
                             .only(*Game.fields_for_game_detail)
        else:
            return self.games.select_related('map').only(*Game.fields_for_game_detail)
    def games_for_lineup(self):
        field_list = Game.fields_for_game_detail + ['home_player__char_code', 'away_player__char_code', 'is_ace']
        defer_list = ['vod', 'replay', 'winner',
                       'home_player__profile__custom_thumb',
                       'home_player__profile__photo',
                       'away_player__profile__custom_thumb',
                       'away_player__profile__photo',
                      ]
        return self.games.select_related('map', 'home_player__team', 'home_player__profile', 'away_player__team', 'away_player__profile') \
                         .only(*field_list).defer(*defer_list)
    def games_played(self):
        return self.games_with_related().exclude(winner_team__isnull=True)
    
    def first_vod(self):
        try:
            return self.games_played()[0].vod
        except IndexError:
            return None
    
    def __unicode__(self):
        return u" ".join((u" vs ".join((unicode(self.home_team), unicode(self.away_team))), date(self.publish_date or self.creation_date, "M d, Y")))
    
    @models.permalink
    def get_absolute_url(self):
        return ('match_page', (), {'tournament': self.tournament_id,
                                  'pk': self.pk,
                                  }
                )
    
def replay_path(instance, filename):
    match = instance.match
    tournament = match.tournament
    filename = "".join(("_".join((unicode(instance.home_player), unicode(instance.away_player), unicode(instance.map))), u".SC2Replay")).encode('ascii', 'ignore')
    return posixpath.join("replays", unicode(tournament), unicode(match), filename)
class Game(models.Model):
    match = models.ForeignKey('Match', related_name="games")
    map = models.ForeignKey('Map') #add verification that this is in map pool for tournament
    order = models.PositiveSmallIntegerField()
    home_player = models.ForeignKey('profiles.TeamMembership', related_name="home_games", null=True, blank=True, on_delete=models.SET_NULL)
    home_race = models.CharField(max_length=1, choices=RACES, blank=True) #TODO: default to player's race in UI
    away_player = models.ForeignKey('profiles.TeamMembership', related_name="away_games", null=True, blank=True, on_delete=models.SET_NULL)
    away_race = models.CharField(max_length=1, choices=RACES, blank=True) #TODO: default to player's race in UI
    winner = models.ForeignKey('profiles.TeamMembership', related_name="game_wins", blank=True, null=True, on_delete=models.SET_NULL)
    loser = models.ForeignKey('profiles.TeamMembership', related_name="game_losses", blank=True, null=True, editable=False, on_delete=models.SET_NULL)
    winner_team = models.ForeignKey('profiles.Team', related_name="game_wins", blank=True, null=True)
    loser_team = models.ForeignKey('profiles.Team', related_name="game_losses", blank=True, null=True, editable=False)
    forfeit = models.BooleanField(default=False)
    replay = models.FileField(upload_to=replay_path, max_length=300, null=True, blank=True)
    vod = models.URLField(blank=True)
    is_ace = models.BooleanField(default=False)
    
    fields_for_game_detail = ['map',
                           'home_player__char_name',
                           'home_race',
                           'home_player__profile__custom_thumb',
                           'home_player__profile__photo',
                           'home_player__profile__slug',
                           'home_player__team__slug',
                           'home_player__team__tournament',
                           'away_player__char_name',
                           'away_race',
                           'away_player__profile__custom_thumb',
                           'away_player__profile__photo',
                           'away_player__profile__slug',
                           'away_player__team__slug',
                           'away_player__team__tournament',
                           'vod',
                           'order',
                           'replay',
                           'winner',
                           'winner_team',
                           ]
    
    # validate winner is one of the players and sets the loser to the other player
    # also set the winner and loser team
    def clean(self):
        super(Game, self).clean()
        from django.core.exceptions import ValidationError
        if self.winner:
            if self.winner_id == self.home_player_id:
                self.loser = self.away_player
                self.winner_team = self.match.home_team
                self.loser_team = self.match.away_team
            elif self.winner_id == self.away_player_id:
                self.loser = self.home_player
                self.winner_team = self.match.away_team
                self.loser_team = self.match.home_team
            else:
                raise ValidationError("Winner must be one of the players playing")
        else:
            self.loser = None
            # in case of team games, player fields won't be set
            if self.winner_team:
                if self.winner_team_id == self.match.home_team_id:
                    self.loser_team = self.match.away_team
                elif self.winner_team_id == self.match.away_team_id:
                    self.loser_team = self.match.home_team
                else:
                    raise ValidationError("Winning team must be one of the teams playing")
            else:
                self.winner_team = None
                self.loser_team = None
        
    # computes match wins
    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)
        total_games = self.match.games.count()
        games = self.match.games.all()
        hwins = len([g for g in games if (g.winner_id and g.home_player_id==g.winner_id) or self.match.home_team_id==g.winner_team_id])
        awins = len([g for g in games if (g.winner_id and g.away_player_id==g.winner_id) or self.match.away_team_id==g.winner_team_id])
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
            ret = ""
            #ret = unicode(self.match)
        return u" on ".join((ret, unicode(self.map_id)))
        
    class Meta:
        unique_together = (('order','match'),)
        ordering = ('order',)

@receiver(post_save, sender=Match, dispatch_uid="tournaments_update_winloss")
def update_winloss(sender, instance, created, **kwargs):
    if instance.published and instance.winner:
        instance.update_winloss()            
    
@receiver(post_save, sender=Match, dispatch_uid="tournaments_update_tiebreaker")
def update_tiebreaker(sender, instance, created, **kwargs):
    instance.update_tiebreaker()

class GamePluginModel(CMSPlugin):
    tournament = models.ForeignKey('Tournament')
    game = models.ForeignKey('Game', blank=True, null=True)
class TournamentPluginModel(CMSPlugin):
    tournament = models.ForeignKey('Tournament')