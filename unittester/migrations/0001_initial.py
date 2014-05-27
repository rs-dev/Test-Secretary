# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UnitTest'
        db.create_table('unittester_unittest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test_module', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
        ))
        db.send_create_signal('unittester', ['UnitTest'])


    def backwards(self, orm):
        # Deleting model 'UnitTest'
        db.delete_table('unittester_unittest')


    models = {
        'unittester.unittest': {
            'Meta': {'object_name': 'UnitTest'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True', 'null': 'True'}),
            'test_module': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        }
    }

    complete_apps = ['unittester']