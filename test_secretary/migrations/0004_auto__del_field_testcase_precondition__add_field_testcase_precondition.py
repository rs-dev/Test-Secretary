# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TestCase.precondition'
        db.delete_column('test_secretary_testcase', 'precondition')

        # Adding field 'TestCase.precondition_comment'
        db.add_column('test_secretary_testcase', 'precondition_comment',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field preconditions on 'TestCase'
        m2m_table_name = db.shorten_name('test_secretary_testcase_preconditions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_testcase', models.ForeignKey(orm['test_secretary.testcase'], null=False)),
            ('to_testcase', models.ForeignKey(orm['test_secretary.testcase'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_testcase_id', 'to_testcase_id'])


    def backwards(self, orm):
        # Adding field 'TestCase.precondition'
        db.add_column('test_secretary_testcase', 'precondition',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'TestCase.precondition_comment'
        db.delete_column('test_secretary_testcase', 'precondition_comment')

        # Removing M2M table for field preconditions on 'TestCase'
        db.delete_table(db.shorten_name('test_secretary_testcase_preconditions'))


    models = {
        'test_secretary.application': {
            'Meta': {'object_name': 'Application', 'ordering': "['name']"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'precondition_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'preconditions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'preconditions_rel_+'", 'to': "orm['test_secretary.TestCase']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['test_secretary.TestSection']"})
        },
        'test_secretary.testcaserun': {
            'Meta': {'object_name': 'TestCaseRun'},
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
            'testcases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'through': "orm['test_secretary.TestCaseRun']", 'to': "orm['test_secretary.TestCase']"}),
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