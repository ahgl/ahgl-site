# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tournament'
        db.create_table('tournaments_tournament', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True, db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tournaments', ['Tournament'])

        # Adding M2M table for field map_pool on 'Tournament'
        db.create_table('tournaments_tournament_map_pool', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tournament', models.ForeignKey(orm['tournaments.tournament'], null=False)),
            ('map', models.ForeignKey(orm['tournaments.map'], null=False))
        ))
        db.create_unique('tournaments_tournament_map_pool', ['tournament_id', 'map_id'])

        # Adding model 'Map'
        db.create_table('tournaments_map', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
        ))
        db.send_create_signal('tournaments', ['Map'])

        # Adding model 'Match'
        db.create_table('tournaments_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_matches', to=orm['profiles.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_matches', to=orm['profiles.Team'])),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matches', to=orm['tournaments.Tournament'])),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('referee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Profile'], null=True, blank=True)),
            ('home_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('away_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tournaments', ['Match'])

        # Adding model 'Game'
        db.create_table('tournaments_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games', to=orm['tournaments.Match'])),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournaments.Map'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('home_player', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='home_games', null=True, to=orm['profiles.Profile'])),
            ('home_race', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('away_player', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='away_games', null=True, to=orm['profiles.Profile'])),
            ('away_race', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('winner', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('forfeit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('replay', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('vod', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('is_ace', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tournaments', ['Game'])

        # Adding unique constraint on 'Game', fields ['order', 'match']
        db.create_unique('tournaments_game', ['order', 'match_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Game', fields ['order', 'match']
        db.delete_unique('tournaments_game', ['order', 'match_id'])

        # Deleting model 'Tournament'
        db.delete_table('tournaments_tournament')

        # Removing M2M table for field map_pool on 'Tournament'
        db.delete_table('tournaments_tournament_map_pool')

        # Deleting model 'Map'
        db.delete_table('tournaments_map')

        # Deleting model 'Match'
        db.delete_table('tournaments_match')

        # Deleting model 'Game'
        db.delete_table('tournaments_game')


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
            'custom_thumb': ('imagekit.models.ProcessedImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('imagekit.models.ProcessedImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'questions_answers': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'profiles.team': {
            'Meta': {'unique_together': "(('name', 'tournament'),)", 'object_name': 'Team'},
            'captain': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'captain_of'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'charity': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'teams'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['profiles.Profile']"}),
            'motto': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('imagekit.models.ProcessedImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': "orm['tournaments.Tournament']"})
        },
        'tournaments.game': {
            'Meta': {'unique_together': "(('order', 'match'),)", 'object_name': 'Game'},
            'away_player': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'away_games'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'away_race': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'forfeit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_player': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'home_games'", 'null': 'True', 'to': "orm['profiles.Profile']"}),
            'home_race': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ace': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournaments.Map']"}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': "orm['tournaments.Match']"}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'replay': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'vod': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'winner': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
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
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'referee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Profile']", 'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['tournaments.Tournament']"})
        },
        'tournaments.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map_pool': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournaments.Map']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['tournaments']
