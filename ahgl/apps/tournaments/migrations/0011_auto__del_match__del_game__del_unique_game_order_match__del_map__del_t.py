# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Game', fields ['order', 'match']
        db.delete_unique('tournaments_game', ['order', 'match_id'])

        # Deleting model 'Match'
        db.delete_table('tournaments_match')

        # Deleting model 'Game'
        db.delete_table('tournaments_game')

        # Deleting model 'Map'
        db.delete_table('tournaments_map')

        # Deleting model 'Tournament'
        db.delete_table('tournaments_tournament')

        # Removing M2M table for field map_pool on 'Tournament'
        db.delete_table('tournaments_tournament_map_pool')


    def backwards(self, orm):
        
        # Adding model 'Match'
        db.create_table('tournaments_match', (
            ('referee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Profile'], null=True, blank=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matches', to=orm['tournaments.Tournament'])),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('away_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_matches', to=orm['profiles.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_matches', to=orm['profiles.Team'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_wins', null=True, to=orm['profiles.Team'], blank=True)),
            ('loser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_losses', null=True, to=orm['profiles.Team'], blank=True)),
            ('home_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tournaments', ['Match'])

        # Adding model 'Game'
        db.create_table('tournaments_game', (
            ('vod', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournaments.Map'])),
            ('loser_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_losses', null=True, to=orm['profiles.Team'], blank=True)),
            ('forfeit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_wins', null=True, to=orm['profiles.Profile'], blank=True)),
            ('loser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_losses', null=True, to=orm['profiles.Profile'], blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('replay', self.gf('django.db.models.fields.files.FileField')(max_length=300, null=True, blank=True)),
            ('away_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_games', null=True, to=orm['profiles.Profile'], blank=True)),
            ('home_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_games', null=True, to=orm['profiles.Profile'], blank=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games', to=orm['tournaments.Match'])),
            ('home_race', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('winner_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_wins', null=True, to=orm['profiles.Team'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_ace', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('away_race', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal('tournaments', ['Game'])

        # Adding unique constraint on 'Game', fields ['order', 'match']
        db.create_unique('tournaments_game', ['order', 'match_id'])

        # Adding model 'Map'
        db.create_table('tournaments_map', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
        ))
        db.send_create_signal('tournaments', ['Map'])

        # Adding model 'Tournament'
        db.create_table('tournaments_tournament', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('featured_game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournaments.Game'], null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True, db_index=True)),
        ))
        db.send_create_signal('tournaments', ['Tournament'])

        # Adding M2M table for field map_pool on 'Tournament'
        db.create_table('tournaments_tournament_map_pool', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tournament', models.ForeignKey(orm['tournaments.tournament'], null=False)),
            ('map', models.ForeignKey(orm['tournaments.map'], null=False))
        ))
        db.create_unique('tournaments_tournament_map_pool', ['tournament_id', 'map_id'])


    models = {
        
    }

    complete_apps = ['tournaments']
