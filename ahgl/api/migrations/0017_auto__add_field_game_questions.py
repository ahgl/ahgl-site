# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.questions'
        db.add_column('api_game', 'questions',
                      self.gf('profiles.fields.HTMLField')(default='<ol><li>\n<p>Why did you choose this race/champion?</p>\n<p>-</p>\n</li>\n<li>\n<p>What do you do for a living?  What do you love about your job?</p>\n<p>-</p>\n</li>\n<li>\n<p>What other hobbies do you have?</p>\n<p>-</p>\n</li>\n<li>\n<p>Why do you play StarCraft/League of Legends?</p>\n<p>-</p>\n</li>\n<li>\n<p>How long have you been playing?</p>\n<p>-</p>\n</li>\n<li>\n<p>What have you done to prepare for the momentous challenge that is the AHGL Tournament?</p>\n<p>-</p>\n</li>\n<li>\n<p>Why is your team going to win?</p>\n<p>-</p>\n</li>\n<li>\n<p>Who is the best player on your team?  Why?</p>\n<p>-</p>\n</li>\n<li>\n<p>Whom do you fear most amongst the competition and why?</p>\n<p>-</p>\n</li>\n</ol>', attributes={'blockquote': ['cite'], 'th': ['colspan'], 'table': ['class'], 'td': ['colspan'], 'a': ['href', 'rel', 'target', 'title', 'data-toggle', 'class'], 'span': ['class'], 'img': ['src', 'alt', 'title', 'style'], 'ul': ['class'], 'li': ['class'], 'q': ['cite'], 'p': ['style'], 'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen'], 'div': ['class', 'id', 'style']}, blank=True, tags=['ol', 'ul', 'li', 'strong', 'em', 'p']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.questions'
        db.delete_column('api_game', 'questions')


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
            'questions': ('profiles.fields.HTMLField', [], {'default': "'<ol><li>\\n<p>Why did you choose this race/champion?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>What do you do for a living?  What do you love about your job?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>What other hobbies do you have?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>Why do you play StarCraft/League of Legends?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>How long have you been playing?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>What have you done to prepare for the momentous challenge that is the AHGL Tournament?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>Why is your team going to win?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>Who is the best player on your team?  Why?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>Whom do you fear most amongst the competition and why?</p>\\n<p>-</p>\\n</li>\\n</ol>'", 'attributes': "{'blockquote': ['cite'], 'th': ['colspan'], 'table': ['class'], 'td': ['colspan'], 'a': ['href', 'rel', 'target', 'title', 'data-toggle', 'class'], 'span': ['class'], 'img': ['src', 'alt', 'title', 'style'], 'ul': ['class'], 'li': ['class'], 'q': ['cite'], 'p': ['style'], 'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen'], 'div': ['class', 'id', 'style']}", 'blank': 'True', 'tags': "['ol', 'ul', 'li', 'strong', 'em', 'p']"}),
            'small_game_thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        'tournaments.map': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Map'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'tournaments.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'game': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['api.Game']", 'unique': 'True', 'null': 'True'}),
            'games_per_match': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'map_pool': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tournaments.Map']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1', 'db_index': 'True'}),
            'structure': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'})
        }
    }

    complete_apps = ['api']