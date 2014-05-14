# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Precondition'
        db.create_table('test_secretary_precondition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testcase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_secretary.TestCase'], related_name='from_testcase')),
            ('precondition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['test_secretary.TestCase'], related_name='precondition')),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
        ))
        db.send_create_signal('test_secretary', ['Precondition'])

        # Deleting field 'TestCase.precondition_comment'
        db.delete_column('test_secretary_testcase', 'precondition_comment')

        # Removing M2M table for field preconditions on 'TestCase'
        db.delete_table(db.shorten_name('test_secretary_testcase_preconditions'))


    def backwards(self, orm):
        # Deleting model 'Precondition'
        db.delete_table('test_secretary_precondition')

        # Adding field 'TestCase.precondition_comment'
        db.add_column('test_secretary_testcase', 'precondition_comment',
                      self.gf('django.db.models.fields.TextField')(blank=True, null=True),
                      keep_default=False)

        # Adding M2M table for field preconditions on 'TestCase'
        m2m_table_name = db.shorten_name('test_secretary_testcase_preconditions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_testcase', models.ForeignKey(orm['test_secretary.testcase'], null=False)),
            ('to_testcase', models.ForeignKey(orm['test_secretary.testcase'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_testcase_id', 'to_testcase_id'])


    models = {
        'test_secretary.application': {
            'Meta': {'ordering': "['name']", 'object_name': 'Application'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'test_secretary.precondition': {
            'Meta': {'object_name': 'Precondition'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precondition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']", 'related_name': "'precondition'"}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestCase']", 'related_name': "'from_testcase'"})
        },
        'test_secretary.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'action': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'expected': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'preconditions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['test_secretary.TestCase']", 'through': "orm['test_secretary.Precondition']", 'related_name': "'precondition_set'"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestSection']"})
        },
        'test_secretary.testcaserun': {
            'Meta': {'ordering': "('testcase__section__app__name', 'testcase__section__order', 'testcase__section__name', 'testcase__number')", 'object_name': 'TestCaseRun'},
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
            'testcases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'through': "orm['test_secretary.TestCaseRun']", 'to': "orm['test_secretary.TestCase']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'test_secretary.testsection': {
            'Meta': {'ordering': "('app', 'order', 'name')", 'object_name': 'TestSection'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['test_secretary']