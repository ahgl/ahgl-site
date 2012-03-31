# coding=utf8
from __future__ import print_function

import re
import urllib2
import posixpath
import lxml.html as html
from lxml.html import tostring
import traceback
import datetime
from optparse import make_option

from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import Q

from apps.tournaments.models import *
from apps.profiles.models import *
from apps.profiles.pipeline.user import *

class Command(BaseCommand):
    args = '<tournament_slug ahgl_url>'
    help = 'Parses ahgl site and loads the data'
    option_list = BaseCommand.option_list + (
        make_option('--whole-team',
            action='store_true',
            dest='whole_team',
            default=False,
            help='Game involves the whole team playing in a game at once'),
        make_option('--team',
            action='store_true',
            dest='team',
            default=False,
            help='Scrape team and player profile information'),
        make_option('--match',
            action='store_true',
            dest='match',
            default=False,
            help='Scrape match information'),
        make_option('--admin',
            action='store_true',
            dest='admin',
            default=False,
            help='Scrape data from admin page'),
        )
    
    first_week_match = datetime.date(2012, 1, 6)
    a_week = datetime.timedelta(weeks=1)
    master_user = User.objects.get(username='master')
    unknown_photo = '/wp-content/themes/AHGL/images/the-unknown.png'
    
    _map_map = {u"Tal’darim Altar": "Tal'Darim Altar", "Tal'Darim Altar":"Tal'Darim Altar", "The Shattered Temple": "Shattered Temple"}
    def coerse_mapname(self, mapname):
        if mapname in self._map_map.keys():
            return self._map_map[mapname]
        return mapname

    def visit_url(self, path, base=None):
        url = posixpath.join(base, path) if base else path
        print("Visiting {0}".format(url), file=self.stdout)
        self.d = d = html.parse(url).getroot()
        d.make_links_absolute()
        return d

    def load_player(self, member_url, team, char_name=None):
        """ Loads player and team membership data, and adds as member to team. Return profile, membership """
        try:
            member_d = self.visit_url(member_url)
        except IOError:
            profile_name = " ".join((word.capitalize() for word in member_url.strip("/").split("/")[-1].split("-")))
            print("Page not found, constructing from {0} name and {1} charname".format(profile_name, char_name))
            # create profile and membership
            profile, created = Profile(name=profile_name, user=self.master_user), True
            profile.save()
            membership = TeamMembership(team=team, profile=profile, char_name=char_name, active=False)
            membership.save()
            return profile, membership
            
        
        if "Player not found in database" in tostring(member_d):
            print("Player not found...skipping", file=self.stdout)
            return
        info_ps = member_d.cssselect('.content-section-1 p')
        info_h3s = member_d.cssselect('.content-section-1 h3')
        profile_name = info_ps[1].text
        if char_name is None:
            char_name = info_ps[4].text
            if "." in char_name:
                char_name = char_name.split(".", 1)[0]
        if Profile.objects.filter(name=profile_name).count():
            profile, created = Profile.objects.get(name=profile_name), False
            membership, membership_created = TeamMembership.objects.get_or_create(team=team, profile=profile, defaults={'char_name': char_name})
            membership.char_name = char_name
        else:
            try:
                membership = TeamMembership.objects.get(team=team, char_name=char_name)
                profile, created = membership.profile, False
            except TeamMembership.DoesNotExist:
                # create profile and membership
                profile, created = Profile(name=profile_name, user=self.master_user), True
                profile.save()
                membership = TeamMembership(team=team, profile=profile, char_name=char_name)
        print(created, file=self.stdout)
        profile.name = profile_name
        member_photo_url = info_ps[0].cssselect('img')[0].get('src')
        if member_photo_url != self.unknown_photo:
            filename = slugify(profile.name) + posixpath.splitext(member_photo_url)[1]
            profile.photo.save(filename, ContentFile(urllib2.urlopen(member_photo_url).read()))
        if info_ps[3].text:
            profile.title = info_ps[3].text
        if info_ps[-1].text: # deal with blank race
            if info_h3s[-1].text.strip().lower() == "champion":
                membership.champion = info_ps[-1].text.strip()
            else:
                try:
                    membership.race = info_ps[-1].text[0].upper()
                    membership.clean_fields()
                except ValidationError:
                    membership.race = None
        try:
            membership.questions_answers = tostring(member_d.cssselect('div.content-section-2 ol')[0])
        except:
            pass
        try:
            profile.full_clean()
        except ValidationError as e:
            print("Profile did not validate! {profile_name} {e}".format(profile_name=profile_name.encode('ascii', 'ignore'), e=e), file=self.stderr)
        else:
            profile.save()
            membership.save()
        return profile, membership
    def load_team(self, team_url, team_name):
        team_d = self.visit_url(team_url)
       
        # load team data
        team, created = Team.objects.get_or_create(tournament=self.tournament, name=team_name, slug=slugify(team_name), defaults={'rank':1})
        print(created, file=self.stdout)
        photo_url = team_d.cssselect('.content-section-1 img')[0].get('src')
        filename = slugify(team_name) + posixpath.splitext(photo_url)[1]
        team.photo.save(filename, ContentFile(urllib2.urlopen(photo_url).read()))
        
        charity_p = team_d.cssselect('.content-section-3 p')[0 if self.tournament.slug == "starcraft-2-season-1" else 1]
        charity_name = charity_p.cssselect('a')[0].text
        charity, created = Charity.objects.get_or_create(name=charity_name)
        charity.link = charity_p.cssselect('a')[0].get('href')
        if not charity.desc:
            print("charity desc")
            charity.desc = charity_p.text_content().strip()[2:] #"".join(list(charity_p.itertext())[1:])
        try:
            charity_photo_url = team_d.cssselect('.content-section-4 img')[0].get('src')
            filename = slugify(charity_name) + posixpath.splitext(charity_photo_url)[1]
            charity.logo.save(filename, ContentFile(urllib2.urlopen(charity_photo_url).read()))
        except IndexError:
            print("{team} did not have expected image section for charity, leaving blank".format(team=team_name), file=self.stderr)
        charity.full_clean()
        charity.save()
        team.charity = charity

        # load profiles of members
        for member_li in team_d.cssselect("ul.player-list-1.cf li"):
            char_name = member_li.cssselect("h2")[0].text
            member_a = member_li.cssselect("a")[0]
            member_url = member_a.get("href")
            player = self.load_player(member_url, team, char_name)
            if player:
                profile, membership = player
                member_thumbnail_url = member_a.cssselect('img')[0].get('src')
                if member_thumbnail_url != self.unknown_photo:
                    filename = slugify(profile.name) + posixpath.splitext(member_thumbnail_url)[1]
                    profile.custom_thumb.save(filename, ContentFile(urllib2.urlopen(member_thumbnail_url).read()))

        team.full_clean()
        team.save()
        return team
    def find_round(self, home_team, away_team, creation_date):
        for round in TournamentRound.objects.filter(teams__pk=home_team.pk).filter(teams__pk=away_team.pk).order_by('stage_order'):
            previous_matchup_count = round.matches.filter(creation_date__lt=creation_date) \
                                                  .filter((Q(home_team=home_team) & Q(away_team=away_team)) | (Q(home_team=away_team) & Q(away_team=home_team))) \
                                                  .count()
            if not previous_matchup_count:
                break
        return round
    def load_match(self, match_url, week=None):
        match_d = self.visit_url(match_url)
        
        if not match_d.cssselect('a.first-title'):
            print("Not a real match....skipping", file=self.stderr)
            return
        home_team = Team.objects.get(slug=slugify(match_d.cssselect('a.first-title')[0].text.strip()), tournament=self.tournament)
        away_team = Team.objects.get(slug=slugify(match_d.cssselect('a.second-title')[0].text.strip()), tournament=self.tournament)
        if week is None:
            week = int(re.search('week[^/]*([\d]+)[^/]*/', match_url).group(1)) - 1
        print("{0} week".format(week), file=self.stdout)
        creation_date = self.first_week_match + self.a_week*week
        round = self.find_round(home_team, away_team, creation_date)
        match, match_created = Match.objects.get_or_create(home_team=home_team, away_team=away_team, creation_date=creation_date, tournament=self.tournament, defaults={'tournament_round':round})
        match.published = True
        match.publish_date = match.creation_date + self.a_week + datetime.timedelta(days=5)
        match.home_submitted = True
        match.away_submitted = True
        
        match.save(notify=False)
        # add games
        for order, game_li in enumerate(match_d.cssselect('li.cf'), start=1):
            map = " ".join(game_li.cssselect('.video-link-container h3')[0].text.split()[3:])
            map = self.coerse_mapname(map.strip())
            # Map creation
            map, created = Map.objects.get_or_create(name=map)
            if created or not map.photo:
                print("Created map {name}".format(name=map.name.encode('ascii', 'ignore')), file=self.stdout)
                map_photo_url = game_li.cssselect('a.video-link > img')[0].get('src')
                filename = slugify(map.name) + posixpath.splitext(map_photo_url)[1]
                map.photo.save(filename, ContentFile(urllib2.urlopen(map_photo_url).read()))
                map.full_clean()
                map.save()
                self.tournament.map_pool.add(map)
            
            # Game creation
            game, game_created = Game.objects.get_or_create(match=match, order=order, defaults={"map":map})
            game.map = map # just assure the current coersed version
            #if game_created:
            #    print("Created game {order}".format(order=order), file=self.stdout)

            # only load players if players play individual games            
            if not self.options['whole_team']:
                home_player = game_li.cssselect('.video-player-link-container h3')[0].text
                away_player = game_li.cssselect('.video-player-link-container.last h3')[0].text
                home_player_url = game_li.cssselect('.video-player-link-container a')[0].get('href')
                away_player_url = game_li.cssselect('.video-player-link-container.last a')[0].get('href')
                members = ("home", "away")
                for team, char_name, url, member in zip((match.home_team, match.away_team), (home_player, away_player), (home_player_url, away_player_url), members):
                    try:
                        setattr(game, "_".join((member, "player")), TeamMembership.objects.get(team=team, char_name__iexact=char_name))
                    except TeamMembership.DoesNotExist:
                        if char_name == "???" or "#" in url:
                            if char_name != "???":
                                print("Player {0} not found...ignoring".format(char_name), file=self.stderr)
                        else:
                            profile, membership = self.load_player(url, team, char_name)
                            setattr(game, "_".join((member, "player")), membership)

            
            vod = game_li.cssselect('.video-link-container > a.video-link')[0].get('href')
            if vod and not "afterhoursgaming.tv" in vod:
                game.vod = vod
            replay_a = game_li.cssselect('.video-link-container > p > a')
            if replay_a:
                self.save_replay(game, replay_a)
            if game.order==5:
                game.is_ace = True
            game.save()
        match.save(notify=False)
        return match

    def save_replay(self, game, replay_a):
        replay_url = replay_a[0].get('href')
        replay_name = replay_path(game, posixpath.basename(replay_url))
        try:
            game.replay.save(replay_name, ContentFile(urllib2.urlopen(replay_url).read()))
        except urllib2.HTTPError:
            print("Replay not found {replay_url}...ignoring".format(replay_url=replay_url), file=self.stderr)

    def create_membership(self, team, char_name, active=True):
        try:
            return TeamMembership.objects.get(team=team, char_name__iexact=char_name), False
        except TeamMembership.DoesNotExist:
            if active:
                profile, created = Profile(name=char_name, user=self.master_user), True #have to use fake name since admin doesn't have names
                profile.save()
                membership = TeamMembership(team=team, profile=profile, char_name=char_name)
                print("Creating player {0}".format(membership.char_name), file=self.stdout)
                membership.save()
                return membership, created
        return None, False

    re_lineup = re.compile(r"((?P<home_name>[^\.]+)\.(?P<home_code>[^\s]+) \((?P<home_race>[\w])\))? \< (?P<map>[^\>]+) \> (\((?P<away_race>[\w])\) (?P<away_name>[^\.]+)\.(?P<away_code>[^\s]+))?")
    re_captain = re.compile(r"(?P<name>[^,]+), (?P<email>[^@]+@[^\.]+\.[^,]+), (?P<char_name>[^\.]+)\.(?P<char_code>[\d]+)")
    def load_lineup(self, lineup_url):
        lineup_d = self.visit_url(lineup_url)
        week = int(lineup_d.cssselect("h1")[0].text.strip().rsplit(None, 1)[-1]) - 1
        matches_needing_games = []
        map_pool = []
        for match_h2, matchup_p, captains_h3 in zip(lineup_d.cssselect("h2"), lineup_d.cssselect("p"), lineup_d.cssselect("h3")[1::3]):
            home_team, away_team = (s.strip() for s in match_h2.text.split(":")[1].split(" vs "))
            home_team = Team.objects.get(name=home_team, tournament=self.tournament)
            away_team = Team.objects.get(name=away_team, tournament=self.tournament)
            
            # set captain flag
            captain_matchers = ((self.re_captain.search(text), team) for text, team in zip(captains_h3.text_content().split("Captains: ", 1)[1].split(" AND ", 1), (home_team, away_team)))
            for cmatch, team in captain_matchers:
                try:
                    try:
                        captain = TeamMembership.objects.get(team=team, char_name__iexact=cmatch.group('char_name'))
                    except TeamMembership.MultipleObjectsReturned:
                        captain = TeamMembership.objects.get(team=team, char_name__iexact=cmatch.group('char_name'), profile__user=self.master_user)
                except TeamMembership.DoesNotExist: # if there is no captain account, create one
                    username = get_username({}, {'name':cmatch.group('name')}, None)['username']
                    cap_user, created = User.objects.get_or_create(email=cmatch.group('email'), defaults={'username':username, 'password':'!'})
                    if created:
                        print("Created new captain user {0}".format(cmatch.group('name')), file=self.stdout)
                    cap_user.first_name, cap_user.last_name = cmatch.group('name').split(None, 1)
                    cap_user.save()
                    captain_profile = cap_user.get_profile()
                    captain_profile.name = cmatch.group('name')
                    captain_profile.save()
                    captain, membership_created = TeamMembership.objects.get_or_create(team=team, profile=captain_profile)
                    captain.char_name = cmatch.group('char_name')
                    captain.char_code = int(cmatch.group('char_code'))
                    captain.save()
                captain.captain = True
                captain.save()
            
            creation_date = self.first_week_match + self.a_week*week
            try: # ug, inconsistencies in ordering....
                match = Match.objects.get(home_team=away_team, away_team=home_team, creation_date=creation_date, tournament=self.tournament)
            except Match.DoesNotExist:
                reverse_order = False
                round = self.find_round(home_team, away_team, creation_date)
                match, match_created = Match.objects.get_or_create(home_team=home_team, away_team=away_team, creation_date=creation_date, tournament=self.tournament, defaults={'tournament_round':round})
                if match_created:
                    print("Creating new match {0} vs {1}".format(home_team, away_team), file=self.stdout)
                else:
                    print("Processing match {0} vs {1}".format(home_team, away_team), file=self.stdout)
            else:
                reverse_order = True
            match.home_submitted = True
            match.away_submitted = True
            
            maps = []
            for order, game_text in enumerate(matchup_p.itertext(), start=1):
                game_matcher = self.re_lineup.search(game_text.strip())
                if not game_matcher:
                    print("Could not match on {0} ...skipping".format(game_text.strip()), file=self.stderr)
                    if "NOT ENTERED" in game_text:
                        match.home_submitted = False
                        match.away_submitted = False
                        matches_needing_games.append(match)
                    continue
                map_name = self.coerse_mapname(game_matcher.group('map').strip())
                map, map_created = Map.objects.get_or_create(name=map_name)
                if map_created:
                    print("{0} map not found...creating".format(map_name), file=self.stderr)
                    self.tournament.map_pool.add(map)
                
                game, game_created = Game.objects.get_or_create(match=match, order=order, defaults={"map":map})
                game.map = map # just assure the current coersed version
                if game_created:
                    print("  Creating new game {0} {1} {2}".format(home_team.name, map_name, away_team.name), file=self.stdout)
                    match.games.add(game)
                if game_matcher.group("away_race"): #not ace match, load up player data
                    p1, p1_created = self.create_membership(team=home_team, char_name=game_matcher.group("home_name"))
                    p2, p2_created = self.create_membership(team=away_team, char_name=game_matcher.group("away_name"))
                    p1race = game_matcher.group("home_race").upper()
                    p2race = game_matcher.group("away_race").upper()
                    if reverse_order:
                        game.home_player = p2
                        game.home_race = p2race
                        game.away_player = p1
                        game.away_race = p1race
                    else:
                        game.home_player = p1
                        game.home_race = p1race
                        game.away_player = p2
                        game.away_race = p2race

                    try:
                        p1.char_code = p1.char_code or int(game_matcher.group("home_code"))
                    except ValueError:
                        pass
                    p1.race = p1.race or p1race
                    try:
                        p2.char_code = p2.char_code or int(game_matcher.group("away_code"))
                    except ValueError:
                        pass
                    p2.race = p2.race or p2race
                    p1.save()
                    p2.save()
                    maps.append((map, False))
                else:
                    game.is_ace = True
                    maps.append((map, True))
                game.save()
            match.save(notify=False)
            if maps:
                map_pool = maps
        if matches_needing_games:
            if map_pool:
                for match in matches_needing_games:
                    print("Match {0} had no map information...using information from other matches".format(match), file=self.stdout)
                    for order, (map, is_ace) in enumerate(map_pool, start=1):
                        game, game_created = Game.objects.get_or_create(match=match, order=order, defaults={"map":map})
                        if game_created:
                            print("Created game on map {0}".format(map.name), file=self.stdout)
                        game.is_ace = is_ace
                        game.full_clean()
                        game.save()
                    match.save(notify=False)
            else:
                print("No map information was gathered for this week, so deleting all matches.", file=self.stdout)
                for match in matches_needing_games:
                    match.delete()
         
    re_result = re.compile("\): (?P<home_name>[^\.:]+)\.(?P<home_code>[^\s]+) \((?P<home_race>[\w])\) (?P<win_ptr>&lt;|&gt;) \((?P<away_race>[\w])\) (?P<away_name>[^\.]+)\.(?P<away_code>[^\s]+)")
    def load_result(self, result_url):
        result_d = self.visit_url(result_url)
        week = int(result_d.cssselect("h1")[0].text.strip().rsplit(None, 1)[-1]) - 1
        for match_h2, matchup_p in zip(result_d.cssselect("h2"), result_d.cssselect("p")[1:]):
            home_team, away_team = (s.strip() for s in match_h2.text.split(":")[1].split(" vs "))
            home_team = Team.objects.get(name=home_team, tournament=self.tournament)
            away_team = Team.objects.get(name=away_team, tournament=self.tournament)
            creation_date = self.first_week_match + self.a_week*week
            try: # ug, inconsistencies in ordering....
                match = Match.objects.get(home_team=away_team, away_team=home_team, creation_date=creation_date, tournament=self.tournament)
            except Match.DoesNotExist:
                reverse_order = False
                try:
                    match = Match.objects.get(home_team=home_team, away_team=away_team, creation_date=creation_date, tournament=self.tournament)
                except Match.DoesNotExist: # this means we didn't have any map data, so we had deleted the matches
                    continue
                print("Processing match {0} vs {1}".format(home_team, away_team), file=self.stdout)
            else:
                reverse_order = True

            match.publish_date = match.creation_date + self.a_week + datetime.timedelta(days=5)
            p_string = tostring(matchup_p)[3:-4]
            for order, game_text in enumerate(p_string.split("<br>")[:-1], start=1):
                if "Not played" not in game_text:
                    try:
                        game = Game.objects.get(match=match, order=order)
                    except Game.DoesNotExist:
                        print("{0} game does not exist...skipping".format(order), file=self.stderr)
                        continue
                    game_matcher = self.re_result.search(game_text.strip())
                    if not game_matcher:
                        print("Could not match on {0} ...skipping".format(game_text.strip()), file=self.stderr)
                        continue
                    try:
                        home_code = int(game_matcher.group("home_code").strip())
                    except ValueError:
                        home_player = TeamMembership.objects.get(char_name__iexact=game_matcher.group("home_name").strip())
                    else:
                        home_player = TeamMembership.objects.get(char_name__iexact=game_matcher.group("home_name").strip(), char_code=home_code)
                    try:
                        away_code = int(game_matcher.group("away_code").strip())
                    except ValueError:
                        away_player = TeamMembership.objects.get(char_name__iexact=game_matcher.group("away_name").strip())
                    else:
                        away_player = TeamMembership.objects.get(char_name__iexact=game_matcher.group("away_name").strip(), char_code=away_code)
                    home_race = game_matcher.group("home_race").upper()
                    away_race = game_matcher.group("away_race").upper()
                    if reverse_order:
                        game.home_player = away_player
                        game.away_player = home_player
                        game.home_race = away_race
                        game.away_race = home_race
                    else:
                        game.home_player = home_player
                        game.away_player = away_player
                        game.home_race = home_race
                        game.away_race = away_race
                    # if the team has already won, this game doesn't count
                    if game_matcher.group("win_ptr") == "&lt;":
                        game.winner = away_player
                    elif game_matcher.group("win_ptr") == "&gt;":
                        game.winner = home_player
                    else:
                        print("Unrecognized game result: {0}".format(game_text), file=self.stdout)
                        continue
                    p = html.fragment_fromstring("<p>"+game_text+"</p>")
                    replay_a = list(p.cssselect("a"))
                    if replay_a:
                        if not game.replay:
                            self.save_replay(game, replay_a)
                    else:
                        assert("forfeit" in game_text)
                        game.forfeit = True
                    game.full_clean()
                    game.save()
            match.remove_extra_victories()

    def handle(self, *args, **options):
        self.options = options
        try:
            self.tournament = Tournament.objects.get(slug=args[0])
        except Tournament.DoesNotExist:
            raise CommandError("Tournament {0} does not exist".format(args[0]))
        self.site_url = args[1] if len(args)>1 else "http://afterhoursgaming.tv/sc2/"
        admin_url = "http://ahgl.thatsnotanimprovement.com/"
        if self.tournament.slug == "starcraft-2-season-1":
            self.first_week_match = datetime.date(2011, 6, 24)
        
        
        settings.INSTALLED_APPS.remove("notification")
        
        try:
            if options['team']:
                # Load teams
                teams_d = self.visit_url("teams", self.site_url)
                for team_li in teams_d.cssselect('.result-list li'):
                    team_a = team_li.cssselect('a')[0]
                    team_url = team_a.get('href')
                    team_name = " ".join(team_a.text_content().strip().split()[:-1])
                    self.load_team(team_url, team_name)
                
            if options['match']:
                # load groups
                schedule_d = self.visit_url("schedule", self.site_url)
                if options['whole_team']:
                    round_lis = schedule_d.cssselect(".season-list-item")[0].cssselect(".week-list-1 .week-list-1")
                else:
                    round_lis = schedule_d.cssselect('#week-1-schedule li.season-list-item')
                for i, group_li in enumerate(round_lis, start=1):
                    round, created = TournamentRound.objects.get_or_create(order=i, stage_order=1, tournament=self.tournament, default={'stage_name':"Group"})
                    print("Round {0} retrieved, adding members".format(i), file=self.stdout)
                    for team_span in group_li.cssselect('.week-list-link > span.f2'):
                        team_slug = slugify(team_span.text.strip())
                        tried_nospace = False
                        while True:
                            try:
                                team = Team.objects.get(slug=team_slug, tournament=self.tournament)
                                round.teams.add(team)
                                print("Team {slug} successfully added".format(slug=team_slug), file=self.stdout)
                                break
                            except Team.DoesNotExist:
                                if not tried_nospace:
                                    print("Team {slug} not found...trying without spaces".format(slug=team_slug), file=self.stdout)
                                    team_slug = team_slug.replace('-','')
                                    tried_nospace = True
                                else:
                                    print("Team {slug} not found................skipping".format(slug=team_slug), file=self.stdout)
                                    break
                        
                # load matches
                for week, week_li in enumerate(schedule_d.cssselect("li.season-list-item")):
                    for match_li in week_li.cssselect('li.week-list-item'):
                        match_url = list(match_li.cssselect('a.week-list-link'))[-1].get('href')
                        self.load_match(match_url, week)
                
            # ----------- Admin site ------------------
            if options['admin']:
                # Load char codes
                roster_d = self.visit_url("view-rosters", admin_url)
                for tr in roster_d.cssselect("table tr"):
                    try:
                        team, player, active = (td.text.strip() for td in tr.cssselect('td')[:3])
                    except ValueError: # on the th line
                        continue
                    char_name, char_code = player.split(".")
                    team = Team.objects.get(name=team, tournament=self.tournament)
                    if active=="0":
                        active = False
                    else:
                        active = True
                    membership, created = self.create_membership(team=team, char_name=char_name, active=active)
                    if membership is None:
                        continue
                    membership.active = active
                    try:
                        membership.char_code = int(char_code)
                        membership.save()
                    except ValueError:
                        pass
                
                # load lineups (extra match info)
                lineup_d = self.visit_url("show-lineup", admin_url)
                for a in lineup_d.cssselect("a"):
                    self.load_lineup(a.get('href'))
                
                # load results
                result_d = self.visit_url("show-result", admin_url)
                for a in result_d.cssselect("a"):
                    self.load_result(a.get('href'))
                
            # ----------- Update stats ------------------
            for team in Team.objects.filter(tournament=self.tournament):
                team.update_stats()
            for membership in TeamRoundMembership.objects.filter(tournamentround__tournament=self.tournament):
                membership.update_stats()
                            
        except Exception as e:
            print('Error occured, dumping last document\n {0}'.format(tostring(self.d) if hasattr(self,"d") else None), file=self.stderr)
            traceback.print_exc(file=self.stderr)
            print(e, file=self.stderr)