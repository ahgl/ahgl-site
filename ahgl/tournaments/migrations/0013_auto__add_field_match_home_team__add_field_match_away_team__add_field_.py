# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    depends_on = (
        ("profiles", "0007_auto__add_team__add_unique_team_name_tournament__add_unique_team_slug_"),
    )

    def forwards(self, orm):
        
        # Adding field 'Match.home_team'
        db.add_column('tournaments_match', 'home_team', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='home_matches', to=orm['profiles.Team']), keep_default=False)

        # Adding field 'Match.away_team'
        db.add_column('tournaments_match', 'away_team', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='away_matches', to=orm['profiles.Team']), keep_default=False)

        # Adding field 'Match.winner'
        db.add_column('tournaments_match', 'winner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='match_wins', null=True, to=orm['profiles.Team']), keep_default=False)

        # Adding field 'Match.loser'
        db.add_column('tournaments_match', 'loser', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='match_losses', null=True, to=orm['profiles.Team']), keep_default=False)

        # Adding field 'Game.winner_team'
        db.add_column('tournaments_game', 'winner_team', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='game_wins', null=True, to=orm['profiles.Team']), keep_default=False)

        # Adding field 'Game.loser_team'
        db.add_column('tournaments_game', 'loser_team', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='game_losses', null=True, to=orm['profiles.Team']), keep_default=False)

        # Adding M2M table for field teams on 'TournamentRound'
        db.create_table('tournaments_tournamentround_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tournamentround', models.ForeignKey(orm['tournaments.tournamentround'], null=False)),
            ('team', models.ForeignKey(orm['profiles.team'], null=False))
        ))
        db.create_unique('tournaments_tournamentround_teams', ['tournamentround_id', 'team_id'])


    def backwards(self, orm):
        
        # Deleting field 'Match.home_team'
        db.delete_column('tournaments_match', 'home_team_id')

        # Deleting field 'Match.away_team'
        db.delete_column('tournaments_match', 'away_team_id')

        # Deleting field 'Match.winner'
        db.delete_column('tournaments_match', 'winner_id')

        # Deleting field 'Match.loser'
        db.delete_column('tournaments_match', 'loser_id')

        # Deleting field 'Game.winner_team'
        db.delete_column('tournaments_game', 'winner_team_id')

        # Deleting field 'Game.loser_team'
        db.delete_column('tournaments_game', 'loser_team_id')

        # Removing M2M table for field teams on 'TournamentRound'
        db.delete_table('tournaments_tournamentround_teams')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'bnet_profile': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'char_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'char_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'custom_thumb': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'questions_answers': ('profiles.fields.HTMLField', [], {'attributes': '[]', 'blank': 'True', 'tags': "['ol', 'ul', 'li', 'strong', 'em', 'p']"}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'profiles.team': {
            'Meta': {'unique_together': "(('name', 'tournament'), ('slug', 'tournament'))", 'object_name': 'Team'},
            'captain': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'captain_of'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'charity': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'teams'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['profiles.Profile']"}),
            'motto': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'seed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tiebreaker': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': "orm['tournaments.Tournament']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'tournaments.game': {
            'Meta': {'ordering': "('order',)", 'unique_together': "(('order', 'match'),)", 'object_name': 'Game'},
            'away_player': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'away_games'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'away_race': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'forfeit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_player': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'home_games'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'home_race': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ace': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_losses'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'loser_team': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_losses'", 'null': 'True', 'to': "orm['profiles.Team']"}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournaments.Map']"}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': "orm['tournaments.Match']"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'replay': ('django.db.models.fields.files.FileField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'vod': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_wins'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'winner_team': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_wins'", 'null': 'True', 'to': "orm['profiles.Team']"})
        },
        'tournaments.map': {
            'Meta': {'object_name': 'Map'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        'tournaments.match': {
            'Meta': {'object_name': 'Match'},
            'away_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matches'", 'to': "orm['profiles.Team']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'home_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matches'", 'to': "orm['profiles.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'match_losses'", 'null': 'True', 'to': "orm['profiles.Team']"}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'referee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Profile']", 'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['tournaments.Tournament']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'match_wins'", 'null': 'True', 'to': "orm['profiles.Team']"})
        },
        'tournaments.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'featured_game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournaments.Game']", 'null': 'True', 'blank': 'True'}),
            'map_pool': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournaments.Map']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'tournaments.tournamentround': {
            'Meta': {'object_name': 'TournamentRound'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'stage': ('django.db.models.fields.IntegerField', [], {}),
            'structure': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '1'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rounds'", 'symmetrical': 'False', 'to': "orm['profiles.Team']"}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': "orm['tournaments.Tournament']"})
        }
    }

    complete_apps = ['tournaments']
