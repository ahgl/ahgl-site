from collections import namedtuple
import posixpath
import logging
import math
from itertools import count, takewhile, groupby
import os.path

from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import date, slugify
from django.utils import timezone

from tinymce.models import HTMLField

from cms.models.pagemodel import Page

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

from profiles import RACES


logger = logging.getLogger(__name__)


def validate_wholenumber(value):
    if value < 1:
        raise ValidationError(u'{0} is not a whole number'.format(value))


class Tournament(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)
    map_pool = models.ManyToManyField('Map')
    status = models.CharField(max_length=1, choices=(('C', 'Completed'), ('A', 'Active'), ('S', 'Signup'),), default='S', db_index=True)
    games_per_match = models.PositiveSmallIntegerField(default=5, verbose_name="Default Games per Match", validators=[validate_wholenumber])
    structure = models.CharField(max_length=1, choices=(('I', 'Individual'), ('T', 'Team'),), default='I')

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
TeamBracketRecord = namedtuple("TeamBracketRecord", "home_team_membership, away_team_membership, match, is_champion")


class TournamentRound(models.Model):
    order = models.IntegerField()
    tournament = models.ForeignKey('Tournament', related_name='rounds')
    teams = models.ManyToManyField('profiles.Team', related_name='rounds', through='TeamRoundMembership')
    stage_order = models.IntegerField()
    stage_name = models.CharField(max_length=40)
    structure = models.CharField(max_length=1, choices=(('G', 'Group'), ('E', 'Elimination'),), default='G')
    published = models.BooleanField(default=False)

    @staticmethod
    def _round_name(count):
        return {1: "Champion",
                2: "Finals",
                4: "Semi-finals"}.get(count) or "Round of {0}".format(count)

    @staticmethod
    def _seed(bracket):
        # this only works for multiples of two
        len_base = math.log(len(bracket), 2)
        if int(len_base) != len_base:
            return []
        fbracket = [(None, 0)] * len(bracket)
        fbracket[0] = bracket[0]
        stage_size = 2
        next_step = len(bracket)
        while stage_size <= len(bracket):
            step = next_step
            next_step = step // 2
            for i in range(0, len(bracket), step):
                fbracket[i + next_step] = bracket[stage_size - fbracket[i][0] - 1]
            stage_size *= 2
        return fbracket

    def match_dict(self):
        queryset = self.matches.filter(published=True).values('id', 'home_team', 'away_team', 'tournament', 'winner', 'games__winner_team').annotate(wins=Count('games')).order_by('home_team', 'away_team')
        keyfunc = lambda match: (match['home_team'], match['away_team'])

        def makematch(match_group):
            ret = None
            for item in match_group:
                ret = ret or item
                if item['games__winner_team']:
                    ret['home_wins' if item['games__winner_team'] == item['home_team'] else 'away_wins'] = item['wins']
            return ret
        return dict((frozenset(key), makematch(match_group)) for key, match_group in groupby(queryset, keyfunc))

    def elim_bracket(self):
        positions, participants = zip(*self._seed(list(enumerate(self.participants()))))
        match_dict = self.match_dict()
        num_players = 0
        for wins_needed in takewhile(lambda x: participants, count(1)):
            num_players = len(participants)
            if num_players == 1:
                yield BracketRow([TeamBracketRecord(participants[0], None, None, True)], self._round_name(num_players))
            else:
                yield BracketRow([TeamBracketRecord(participants[i], participants[i + 1], match_dict.get(frozenset((member.team_id for member in participants[i:i + 2]))), False) for i in range(0, num_players // 2 * 2, 2)], self._round_name(num_players))
            participants = [team_membership for team_membership in participants if team_membership.wins >= wins_needed]
        num_players = num_players // 2
        while num_players:
            if num_players == 1:
                yield BracketRow([TeamBracketRecord(None, None, None, True)], self._round_name(num_players))
            else:
                yield BracketRow([TeamBracketRecord(None, None, None, False)] * (num_players // 2), self._round_name(num_players))
            num_players = num_players // 2

    def participants(self):
        queryset = self.team_membership.select_related('team')
        if self.structure == "G":
            return queryset.order_by('-wins', '-tiebreaker', 'team__seed')
        else:
            return queryset.order_by('team__seed')

    def __unicode__(self):
        return " : ".join((self.stage_name, unicode(self.order)))

    class Meta:
        ordering = ('-stage_order', 'order',)


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
        self.tiebreaker = (self.team.game_wins.filter(match__published=True, match__tournament_round=self.tournamentround).count()
                           - self.team.game_losses.filter(match__published=True, match__tournament_round=self.tournamentround).count())
        self.__class__.objects.filter(pk=self.pk).update(wins=self.wins, losses=self.losses, tiebreaker=self.tiebreaker)

    class Meta:
        db_table = 'tournaments_tournamentround_teams'
        unique_together = (('tournamentround', 'team'),)
        auto_created = True  # LOL, this is a terrible hack that keeps add and remove around; only use this if all fields are auto


class Match(models.Model):
    structure = models.CharField(max_length=1, choices=(('I', 'Individual'), ('T', 'Team'),), default='I')
    home_team = models.ForeignKey('profiles.Team', related_name="home_matches")
    away_team = models.ForeignKey('profiles.Team', related_name="away_matches")
    tournament = models.ForeignKey('Tournament', related_name='matches')
    tournament_round = models.ForeignKey('TournamentRound', related_name='matches')
    published = models.BooleanField(default=False)
    publish_date = models.DateField(blank=True, null=True)  # set this when published
    creation_date = models.DateField()
    description = models.TextField(blank=True)
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
                membership.tiebreaker = (team.game_wins.filter(match__published=True, match__tournament_round=self.tournament_round).count()
                                         - team.game_losses.filter(match__published=True, match__tournament_round=self.tournament_round).count())
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
        win_point = (len(games) // 2) + 1
        for game in games:
            # if someone already has the games to win (not counting this one) - this game does not matter
            if (home_wins >= win_point or away_wins >= win_point) and (game.winner or game.winner_team):
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
        if created and not self.creation_date:  # set creation date if it wasn't set already
            self.creation_date = timezone.now()
        if self.published and not self.publish_date:
            self.publish_date = timezone.now()
        super(Match, self).save(*args, **kwargs)
        if "notification" in settings.INSTALLED_APPS and notification and created and notify:
            send_task("tournaments.tasks.notify_match_creation", [unicode(self),
                                                                  self.home_team_id,
                                                                  self.away_team_id, ])

    def delete(self, *args, **kwargs):
        """Note this doesn't get called in bulk delete!"""
        ret = super(Match, self).delete(*args, **kwargs)
        for team in (self.home_team, self.away_team):
            if team:
                team.update_stats()
        return ret

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
                      'away_player__profile__photo', ]
        return self.games.select_related('map', 'home_player__team', 'home_player__profile', 'away_player__team', 'away_player__profile') \
                         .only(*field_list).defer(*defer_list)

    def games_played(self):
        return self.games_with_related().exclude(winner_team__isnull=True)

    def first_vod(self):
        try:
            return self.games_played()[0].vod
        except IndexError:
            return None

    def name(self):
        return u" : ".join((unicode(self.tournament), u" vs ".join((unicode(self.home_team.name), unicode(self.away_team.name)))))

    def winner__name(self):
        return self.winner.name

    def __unicode__(self):
        return u" ".join((unicode(self.tournament), u" vs ".join((unicode(self.home_team.name), unicode(self.away_team.name))), date(self.publish_date or self.creation_date, "M d, Y")))

    @models.permalink
    def get_absolute_url(self):
        return ('match_page', (), {'tournament': self.tournament_id,
                                   'pk': self.pk})

    class Meta:
        verbose_name_plural = "matches"


def replay_path(instance, filename):
    match = instance.match
    tournament = match.tournament
    filename = "".join(("_".join((slugify(unicode(instance.home_player)), slugify(unicode(instance.away_player)), slugify(unicode(instance.map)))), os.path.splitext(filename)[1])).encode('ascii', 'ignore')
    return posixpath.join("replays", unicode(tournament), unicode(match), filename)


def victory_path(instance, filename):
    match = instance.match
    tournament = match.tournament
    filename = "".join(("_".join((unicode(instance.home_player), unicode(instance.away_player), unicode(instance.map))), os.path.splitext(filename)[1])).encode('ascii', 'ignore')
    return posixpath.join("victory", unicode(tournament), unicode(match), filename)


class Game(models.Model):
    match = models.ForeignKey('Match', related_name="games")
    map = models.ForeignKey('Map')  # add verification that this is in map pool for tournament
    order = models.PositiveSmallIntegerField()
    home_player = models.ForeignKey('profiles.TeamMembership', related_name="home_games", null=True, blank=True, on_delete=models.SET_NULL)
    home_race = models.CharField(max_length=1, choices=RACES, blank=True)  # TODO: default to player's race in UI
    away_player = models.ForeignKey('profiles.TeamMembership', related_name="away_games", null=True, blank=True, on_delete=models.SET_NULL)
    away_race = models.CharField(max_length=1, choices=RACES, blank=True)  # TODO: default to player's race in UI
    winner = models.ForeignKey('profiles.TeamMembership', related_name="game_wins", blank=True, null=True, on_delete=models.SET_NULL)
    loser = models.ForeignKey('profiles.TeamMembership', related_name="game_losses", blank=True, null=True, editable=False, on_delete=models.SET_NULL)
    winner_team = models.ForeignKey('profiles.Team', related_name="game_wins", blank=True, null=True)
    loser_team = models.ForeignKey('profiles.Team', related_name="game_losses", blank=True, null=True, editable=False)
    forfeit = models.BooleanField(default=False)
    replay = models.FileField(upload_to=replay_path, max_length=300, null=True, blank=True)
    vod = models.URLField(blank=True)
    is_ace = models.BooleanField(default=False)
    victory_screen = models.ImageField(upload_to=victory_path, max_length=300, null=True, blank=True)

    fields_for_game_detail = ['map', 'home_player__char_name', 'home_race',
                              'home_player__profile__custom_thumb',
                              'home_player__profile__photo',
                              'home_player__profile__slug',
                              'home_player__team__slug',
                              'home_player__team__tournament',
                              'away_player__char_name', 'away_race',
                              'away_player__profile__custom_thumb',
                              'away_player__profile__photo',
                              'away_player__profile__slug',
                              'away_player__team__slug',
                              'away_player__team__tournament', 'vod', 'order',
                              'replay', 'winner', 'winner_team', ]

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
            if self.winner_team and self.match.structure == "T":
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
        hwins = len([g for g in games if (g.winner_id and g.home_player_id == g.winner_id) or self.match.home_team_id == g.winner_team_id])
        awins = len([g for g in games if (g.winner_id and g.away_player_id == g.winner_id) or self.match.away_team_id == g.winner_team_id])
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
        return u" on ".join((ret, unicode(self.map_id)))

    class Meta:
        unique_together = (('order', 'match'),)
        ordering = ('order',)

class Article(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    summary = HTMLField(blank=True)
    published = models.BooleanField(default=False)
    tournaments = models.ManyToManyField('Tournament', related_name='articles')
    publish_date = models.DateField(blank=True, null=True)  # set this when published
    creation_date = models.DateField()

    def __unicode__(self):
        return self.title

    def save(self, notify=True, *args, **kwargs):
        created = self.id is None
        if created and not self.creation_date:  # set creation date if it wasn't set already
            self.creation_date = timezone.now()

        if self.published and not self.publish_date:
            self.publish_date = timezone.now()

        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.cms_plugin.get().page.get_absolute_url()


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

class ArticlePluginModel(CMSPlugin):
    article = models.ForeignKey('Article', unique=True, related_name='cms_plugin')

