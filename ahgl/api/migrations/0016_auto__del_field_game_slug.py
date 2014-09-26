# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Game.slug'
        db.delete_column('api_game', 'slug')


    def backwards(self, orm):
        # Adding field 'Game.slug'
        db.add_column('api_game', 'slug',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    models = {
        'api.carouselitem': {
            'Meta': {'object_name': 'CarouselItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'tournaments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'carousel_items'", 'symmetrical': 'False', 'to': "orm['tournaments.Tournament']"})
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
            'header_image_glow_hex_color': ('api.fields.ColourField', [], {'max_length': '7'}),
            'header_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'icon_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_stream_section_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'match_section_image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'small_game_thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        'tournaments.map': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Map'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'tournaments.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['api.Game']", 'null': 'True'}),
            'games_per_match': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'map_pool': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournaments.Map']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1', 'db_index': 'True'}),
            'structure': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'})
        }
    }

    complete_apps = ['api']