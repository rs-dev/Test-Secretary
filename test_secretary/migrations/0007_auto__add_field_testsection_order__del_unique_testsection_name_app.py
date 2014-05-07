# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'TestSection', fields ['name', 'app']
        db.delete_unique('test_secretary_testsection', ['name', 'app_id'])

        # Adding field 'TestSection.order'
        db.add_column('test_secretary_testsection', 'order',
                      self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TestSection.order'
        db.delete_column('test_secretary_testsection', 'order')

        # Adding unique constraint on 'TestSection', fields ['name', 'app']
        db.create_unique('test_secretary_testsection', ['name', 'app_id'])


    models = {
        'test_secretary.application': {
            'Meta': {'object_name': 'Application', 'ordering': "['name']"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'test_secretary.testcase': {
            'Meta': {'object_name': 'TestCase', 'unique_together': "(('number', 'section'),)"},
            'action': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'expected': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'precondition_comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'preconditions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['test_secretary.TestCase']", 'related_name': "'preconditions_rel_+'"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestSection']"})
        },
        'test_secretary.testcaserun': {
            'Meta': {'object_name': 'TestCaseRun', 'ordering': "('testcase__section__app__name', 'testcase__section__order', 'testcase__section__name', 'testcase__number')"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3', 'default': "'NT'"}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']"}),
            'testrun': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestRun']"})
        },
        'test_secretary.testrun': {
            'Meta': {'object_name': 'TestRun', 'ordering': "['-date']"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'testcases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['test_secretary.TestCase']", 'through': "orm['test_secretary.TestCaseRun']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'test_secretary.testsection': {
            'Meta': {'object_name': 'TestSection', 'ordering': "('app', 'order', 'name')"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['test_secretary']