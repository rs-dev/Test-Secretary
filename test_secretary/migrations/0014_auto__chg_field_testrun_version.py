# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TestRun.version'
        db.alter_column('test_secretary_testrun', 'version', self.gf('django.db.models.fields.CharField')(max_length=40))

    def backwards(self, orm):

        # Changing field 'TestRun.version'
        db.alter_column('test_secretary_testrun', 'version', self.gf('django.db.models.fields.CharField')(max_length=15))

    models = {
        'test_secretary.application': {
            'Meta': {'object_name': 'Application', 'ordering': "['order', 'name']"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'test_secretary.precondition': {
            'Meta': {'object_name': 'Precondition'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precondition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'precondition'", 'to': "orm['test_secretary.TestCase']"}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_testcase'", 'to': "orm['test_secretary.TestCase']"})
        },
        'test_secretary.testcase': {
            'Meta': {'object_name': 'TestCase', 'ordering': "('section', 'number', 'name')"},
            'action': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preconditions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['test_secretary.TestCase']", 'null': 'True', 'blank': 'True', 'related_name': "'precondition_set'", 'symmetrical': 'False', 'through': "orm['test_secretary.Precondition']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestSection']"})
        },
        'test_secretary.testcaserun': {
            'Meta': {'object_name': 'TestCaseRun', 'ordering': "('testcase__section__app__name', 'testcase__section__order', 'testcase__section__name', 'testcase__number')"},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NT'", 'max_length': '3'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']"}),
            'testrun': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestRun']"})
        },
        'test_secretary.testrun': {
            'Meta': {'object_name': 'TestRun', 'ordering': "['-date']"},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'testcases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['test_secretary.TestCase']", 'through': "orm['test_secretary.TestCaseRun']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'test_secretary.testsection': {
            'Meta': {'object_name': 'TestSection', 'ordering': "('app', 'order', 'name')"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['test_secretary']