# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UnitTestRun'
        db.create_table('unittester_unittestrun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unittest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['unittester.UnitTest'])),
            ('testcaserun', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_secretary.TestCaseRun'])),
            ('errors', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('failures', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('success', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('unittester', ['UnitTestRun'])

        # Adding M2M table for field testcases on 'UnitTest'
        m2m_table_name = db.shorten_name('unittester_unittest_testcases')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('unittest', models.ForeignKey(orm['unittester.unittest'], null=False)),
            ('testcase', models.ForeignKey(orm['test_secretary.testcase'], null=False))
        ))
        db.create_unique(m2m_table_name, ['unittest_id', 'testcase_id'])


    def backwards(self, orm):
        # Deleting model 'UnitTestRun'
        db.delete_table('unittester_unittestrun')

        # Removing M2M table for field testcases on 'UnitTest'
        db.delete_table(db.shorten_name('unittester_unittest_testcases'))


    models = {
        'test_secretary.application': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Application'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'test_secretary.precondition': {
            'Meta': {'object_name': 'Precondition'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precondition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']", 'related_name': "'precondition'"}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']", 'related_name': "'from_testcase'"})
        },
        'test_secretary.testcase': {
            'Meta': {'ordering': "('section', 'number', 'name')", 'object_name': 'TestCase'},
            'action': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'preconditions': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'to': "orm['test_secretary.TestCase']", 'through': "orm['test_secretary.Precondition']", 'blank': 'True', 'symmetrical': 'False', 'related_name': "'precondition_set'"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestSection']"})
        },
        'test_secretary.testcaserun': {
            'Meta': {'ordering': "('testcase__section__app__name', 'testcase__section__order', 'testcase__section__name', 'testcase__number')", 'object_name': 'TestCaseRun'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3', 'default': "'NT'"}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']"}),
            'testrun': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestRun']"})
        },
        'test_secretary.testrun': {
            'Meta': {'ordering': "['-date']", 'object_name': 'TestRun'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'testcases': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['test_secretary.TestCase']", 'symmetrical': 'False', 'through': "orm['test_secretary.TestCaseRun']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'test_secretary.testsection': {
            'Meta': {'ordering': "('app', 'order', 'name')", 'object_name': 'TestSection'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'unittester.unittest': {
            'Meta': {'object_name': 'UnitTest'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            'test_module': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'testcases': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'symmetrical': 'False', 'to': "orm['test_secretary.TestCase']"})
        },
        'unittester.unittestrun': {
            'Meta': {'object_name': 'UnitTestRun'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'errors': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'failures': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'success': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'testcaserun': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCaseRun']"}),
            'unittest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['unittester.UnitTest']"})
        }
    }

    complete_apps = ['unittester']