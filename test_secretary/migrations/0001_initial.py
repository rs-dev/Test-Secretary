# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table('test_secretary_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('test_secretary', ['Application'])

        # Adding model 'TestSection'
        db.create_table('test_secretary_testsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_secretary.Application'])),
        ))
        db.send_create_signal('test_secretary', ['TestSection'])

        # Adding model 'TestCase'
        db.create_table('test_secretary_testcase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_secretary.TestSection'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('precondition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('expected', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('test_secretary', ['TestCase'])

        # Adding model 'TestRun'
        db.create_table('test_secretary_testrun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('test_secretary', ['TestRun'])

        # Adding model 'TestCaseRun'
        db.create_table('test_secretary_testcaserun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testcase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_secretary.TestCase'])),
            ('testrun', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_secretary.TestRun'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3, default='NT')),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('test_secretary', ['TestCaseRun'])


    def backwards(self, orm):
        # Deleting model 'Application'
        db.delete_table('test_secretary_application')

        # Deleting model 'TestSection'
        db.delete_table('test_secretary_testsection')

        # Deleting model 'TestCase'
        db.delete_table('test_secretary_testcase')

        # Deleting model 'TestRun'
        db.delete_table('test_secretary_testrun')

        # Deleting model 'TestCaseRun'
        db.delete_table('test_secretary_testcaserun')


    models = {
        'test_secretary.application': {
            'Meta': {'object_name': 'Application'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'test_secretary.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'action': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'precondition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestSection']"})
        },
        'test_secretary.testcaserun': {
            'Meta': {'object_name': 'TestCaseRun'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3', 'default': "'NT'"}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']"}),
            'testrun': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestRun']"})
        },
        'test_secretary.testrun': {
            'Meta': {'object_name': 'TestRun'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'testcases': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['test_secretary.TestCase']", 'through': "orm['test_secretary.TestCaseRun']", 'symmetrical': 'False'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'test_secretary.testsection': {
            'Meta': {'object_name': 'TestSection'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['test_secretary']