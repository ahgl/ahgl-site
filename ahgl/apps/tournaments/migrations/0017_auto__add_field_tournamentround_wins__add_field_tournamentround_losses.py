# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'TeamRoundMembership.wins'
        db.add_column('tournaments_tournamentround_teams', 'wins', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'TeamRoundMembership.losses'
        db.add_column('tournaments_tournamentround_teams', 'losses', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'TeamRoundMembership.tiebreaker'
        db.add_column('tournaments_tournamentround_teams', 'tiebreaker', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Changing field 'Match.creation_date'
        db.alter_column('tournaments_match', 'creation_date', self.gf('django.db.models.fields.DateField')())


    def backwards(self, orm):
        
        # Deleting field 'TeamRoundMembership.wins'
        db.delete_column('tournaments_tournamentround_teams', 'wins')

        # Deleting field 'TeamRoundMembership.losses'
        db.delete_column('tournaments_tournamentround_teams', 'losses')

        # Deleting field 'TeamRoundMembership.tiebreaker'
        db.delete_column('tournaments_tournamentround_teams', 'tiebreaker')

        # Changing field 'Match.creation_date'
        db.alter_column('tournaments_match', 'creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True))


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
        'profiles.charity': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Charity'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'autosubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'avatar': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bnet_profile': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'char_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'char_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'custom_thumb': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'questions_answers': ('profiles.fields.HTMLField', [], {'attributes': '[]', 'blank': 'True', 'tags': "['ol', 'ul', 'li', 'strong', 'em', 'p']"}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'show_signatures': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'signature_html': ('django.db.models.fields.TextField', [], {'max_length': '1054', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '3.0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'profiles.team': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'tournament'), ('slug', 'tournament'))", 'object_name': 'Team'},
            'captain': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'captain_of'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'charity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'teams'", 'null': 'True', 'to': "orm['profiles.Charity']"}),
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
            'Meta': {'ordering': "('name',)", 'object_name': 'Map'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'tournaments.match': {
            'Meta': {'object_name': 'Match'},
            'away_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matches'", 'to': "orm['profiles.Team']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
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
            'games_per_match': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'map_pool': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournaments.Map']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'tournaments.tournamentround': {
            'Meta': {'ordering': "('stage', 'name')", 'object_name': 'TournamentRound'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'stage': ('django.db.models.fields.IntegerField', [], {}),
            'structure': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '1'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rounds'", 'symmetrical': 'False', 'to': "orm['profiles.Team']"}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': "orm['tournaments.Tournament']"}),
        }
    }

    complete_apps = ['tournaments']
