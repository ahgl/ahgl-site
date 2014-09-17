# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Channel'
        db.create_table('api_channel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='channel_names', to=orm['api.Game'])),
        ))
        db.send_create_signal('api', ['Channel'])

        # Deleting field 'Game.channel_name'
        db.delete_column('api_game', 'channel_name')

        # Adding field 'Game.small_game_thumbnail'
        db.add_column('api_game', 'small_game_thumbnail',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2048),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Channel'
        db.delete_table('api_channel')

        # Adding field 'Game.channel_name'
        db.add_column('api_game', 'channel_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Deleting field 'Game.small_game_thumbnail'
        db.delete_column('api_game', 'small_game_thumbnail')


    models = {
        'api.carouselitem': {
            'Meta': {'object_name': 'CarouselItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        'api.channel': {
            'Meta': {'object_name': 'Channel'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'channel_names'", 'to': "orm['api.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'api.game': {
            'Meta': {'object_name': 'Game'},
            'article_section_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'background_match_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'header_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'icon_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_stream_section_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'match_section_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'small_game_thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['api']