# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'TestCase', fields ['number', 'section']
        db.create_unique('test_secretary_testcase', ['number', 'section_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TestCase', fields ['number', 'section']
        db.delete_unique('test_secretary_testcase', ['number', 'section_id'])


    models = {
        'test_secretary.application': {
            'Meta': {'ordering': "['name']", 'object_name': 'Application'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'test_secretary.testcase': {
            'Meta': {'unique_together': "(('number', 'section'),)", 'object_name': 'TestCase'},
            'action': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'expected': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'precondition_comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'preconditions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['test_secretary.TestCase']", 'related_name': "'preconditions_rel_+'"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestSection']"})
        },
        'test_secretary.testcaserun': {
            'Meta': {'object_name': 'TestCaseRun'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NT'", 'max_length': '3'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']"}),
            'testrun': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestRun']"})
        },
        'test_secretary.testrun': {
            'Meta': {'ordering': "['-date']", 'object_name': 'TestRun'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'testcases': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['test_secretary.TestCaseRun']", 'to': "orm['test_secretary.TestCase']", 'symmetrical': 'False'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'test_secretary.testsection': {
            'Meta': {'object_name': 'TestSection'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['test_secretary']