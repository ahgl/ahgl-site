# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Game.live_stream_image_url'
        #db.delete_column('api_game', 'live_stream_image_url')

        # Deleting field 'Game.image_url'
        #db.delete_column('api_game', 'image_url')

        # Deleting field 'Game.featured_match_image_url'
        #db.delete_column('api_game', 'featured_match_image_url')

        # Adding field 'Game.header_image_url'
        #db.add_column('api_game', 'header_image_url',
        #              self.gf('django.db.models.fields.CharField')(default='', max_length=2048),
        #              keep_default=False)

        # Adding field 'Game.section_image_url'
        #db.add_column('api_game', 'section_image_url',
        #              self.gf('django.db.models.fields.CharField')(default='', max_length=2048),
        #              keep_default=False)

        # Adding field 'Game.background_match_image_url'
        #db.add_column('api_game', 'background_match_image_url',
        #              self.gf('django.db.models.fields.CharField')(default='', max_length=2048),
        #              keep_default=False)

        # Adding field 'Game.icon_image_url'
        #db.add_column('api_game', 'icon_image_url',
        #              self.gf('django.db.models.fields.CharField')(default='', max_length=2048),
        #              keep_default=False)
        ""

    def backwards(self, orm):
        # Adding field 'Game.live_stream_image_url'
        db.add_column('api_game', 'live_stream_image_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2048),
                      keep_default=False)

        # Adding field 'Game.image_url'
        db.add_column('api_game', 'image_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2048),
                      keep_default=False)

        # Adding field 'Game.featured_match_image_url'
        db.add_column('api_game', 'featured_match_image_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2048),
                      keep_default=False)

        # Deleting field 'Game.header_image_url'
        db.delete_column('api_game', 'header_image_url')

        # Deleting field 'Game.section_image_url'
        db.delete_column('api_game', 'section_image_url')

        # Deleting field 'Game.background_match_image_url'
        db.delete_column('api_game', 'background_match_image_url')

        # Deleting field 'Game.icon_image_url'
        db.delete_column('api_game', 'icon_image_url')


    models = {
        'api.carouselitem': {
            'Meta': {'object_name': 'CarouselItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        'api.game': {
            'Meta': {'object_name': 'Game'},
            'background_match_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'channel_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'header_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'icon_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'section_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournaments.Tournament']"})
        },
        'tournaments.map': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Map'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'tournaments.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'games_per_match': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'map_pool': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournaments.Map']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1', 'db_index': 'True'}),
            'structure': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'})
        }
    }

    complete_apps = ['api']