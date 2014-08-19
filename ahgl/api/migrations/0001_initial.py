# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table('api_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
        ))
        db.send_create_signal('api', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Game'
        db.delete_table('api_game')


    models = {
        'api.game': {
            'Meta': {'object_name': 'Game'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['api']