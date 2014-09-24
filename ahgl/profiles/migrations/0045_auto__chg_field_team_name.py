# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Team.name'
        db.alter_column('profiles_team', 'name', self.gf('django.db.models.fields.CharField')(max_length=35))

    def backwards(self, orm):

        # Changing field 'Team.name'
        db.alter_column('profiles_team', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
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
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'small_game_thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
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
        'profiles.caster': {
            'Meta': {'object_name': 'Caster'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('profiles.fields.HTMLField', [], {'attributes': "{'blockquote': ['cite'], 'th': ['colspan'], 'table': ['class'], 'td': ['colspan'], 'a': ['href', 'rel', 'target', 'title', 'data-toggle', 'class'], 'span': ['class'], 'img': ['src', 'alt', 'title', 'style'], 'ul': ['class'], 'li': ['class'], 'q': ['cite'], 'p': ['style'], 'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen'], 'div': ['class', 'id', 'style']}", 'blank': 'True', 'tags': "['a', 'abbr', 'acronym', 'blockquote', 'br', 'cite', 'code', 'dd', 'del', 'div', 'dl', 'dt', 'em', 'h2', 'h3', 'h4', 'h5', 'i', 'iframe', 'img', 'ins', 'li', 'ol', 'p', 'pre', 'q', 'small', 'span', 'strong', 'sub', 'sup', 'table', 'td', 'th', 'tr', 'u', 'ul']"}),
            'featured_match': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'casters'", 'null': 'True', 'to': "orm['tournaments.Match']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'casters'", 'to': "orm['tournaments.Tournament']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'caster_profile'", 'to': "orm['auth.User']"})
        },
        'profiles.charity': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Charity'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'autosubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'avatar': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'custom_thumb': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'show_signatures': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'signature_html': ('django.db.models.fields.TextField', [], {'max_length': '1054', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '3.0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'profiles.team': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'tournament'), ('slug', 'tournament'))", 'object_name': 'Team'},
            'approval': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'charity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'teams'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['profiles.Charity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'karma': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teams'", 'to': "orm['profiles.Profile']", 'through': "orm['profiles.TeamMembership']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'motto': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'seed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1'}),
            'tiebreaker': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': "orm['tournaments.Tournament']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'profiles.teammemberinvite': {
            'Meta': {'unique_together': "(('email', 'team'),)", 'object_name': 'TeamMemberInvite'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '15'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_invites'", 'to': "orm['profiles.Team']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'profiles.teammembership': {
            'Meta': {'ordering': "('-active', '-captain', 'char_name')", 'unique_together': "(('team', 'profile'),)", 'object_name': 'TeamMembership', 'db_table': "'profiles_team_members'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'captain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'champion': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'char_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'char_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'game_profile': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_membership'", 'to': "orm['profiles.Profile']"}),
            'questions_answers': ('profiles.fields.HTMLField', [], {'default': "'<ol><li>\\n<p>Why did you choose this race/champion?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>What do you do for a living?  What do you love about your job?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>What other hobbies do you have?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>Why do you play StarCraft/League of Legends?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>How long have you been playing?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>What have you done to prepare for the momentous challenge that is the AHGL Tournament?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>Why is your team going to win?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>Who is the best player on your team?  Why?</p>\\n<p>-</p>\\n</li>\\n<li>\\n<p>Whom do you fear most amongst the competition and why?</p>\\n<p>-</p>\\n</li>\\n</ol>'", 'attributes': "{'blockquote': ['cite'], 'th': ['colspan'], 'table': ['class'], 'td': ['colspan'], 'a': ['href', 'rel', 'target', 'title', 'data-toggle', 'class'], 'span': ['class'], 'img': ['src', 'alt', 'title', 'style'], 'ul': ['class'], 'li': ['class'], 'q': ['cite'], 'p': ['style'], 'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen'], 'div': ['class', 'id', 'style']}", 'blank': 'True', 'tags': "['ol', 'ul', 'li', 'strong', 'em', 'p']"}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_membership'", 'to': "orm['profiles.Team']"})
        },
        'tournaments.map': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Map'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'tournaments.match': {
            'Meta': {'object_name': 'Match'},
            'away_submission_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'away_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_matches'", 'to': "orm['profiles.Team']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_submission_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'home_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_matches'", 'to': "orm['profiles.Team']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'match_losses'", 'null': 'True', 'to': "orm['profiles.Team']"}),
            'publish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'referee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Profile']", 'null': 'True', 'blank': 'True'}),
            'structure': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['tournaments.Tournament']"}),
            'tournament_round': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['tournaments.TournamentRound']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'match_wins'", 'null': 'True', 'to': "orm['profiles.Team']"})
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
        },
        'tournaments.tournamentround': {
            'Meta': {'ordering': "('-stage_order', 'order')", 'object_name': 'TournamentRound'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stage_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'stage_order': ('django.db.models.fields.IntegerField', [], {}),
            'structure': ('django.db.models.fields.CharField', [], {'default': "'G'", 'max_length': '1'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rounds'", 'symmetrical': 'False', 'to': "orm['profiles.Team']"}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rounds'", 'to': "orm['tournaments.Tournament']"})
        }
    }

    complete_apps = ['profiles']