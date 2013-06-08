# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CoreHost.name'
        db.delete_column('sitecontrol_corehost', 'name')

        # Adding field 'CoreHost.host'
        db.add_column('sitecontrol_corehost', 'host',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'PageChecks.path'
        db.add_column('sitecontrol_pagechecks', 'path',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'CoreHost.name'
        raise RuntimeError("Cannot reverse this migration. 'CoreHost.name' and its values cannot be restored.")
        # Deleting field 'CoreHost.host'
        db.delete_column('sitecontrol_corehost', 'host')

        # Deleting field 'PageChecks.path'
        db.delete_column('sitecontrol_pagechecks', 'path')


    models = {
        'sitecontrol.corehost': {
            'Meta': {'object_name': 'CoreHost'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sitecontrol.coresite': {
            'Meta': {'object_name': 'CoreSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'root': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sitecontrol.CoreSource']"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sitecontrol.coresource': {
            'Meta': {'object_name': 'CoreSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sitecontrol.deploycommand': {
            'Meta': {'ordering': "('order',)", 'object_name': 'DeployCommand'},
            'arguments': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'program': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sitecontrol.CoreSite']"})
        },
        'sitecontrol.gitsource': {
            'Meta': {'object_name': 'GitSource', '_ormbases': ['sitecontrol.CoreSource']},
            'coresource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sitecontrol.CoreSource']", 'unique': 'True', 'primary_key': 'True'}),
            'poll_period_minutes': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'sitecontrol.nullsource': {
            'Meta': {'object_name': 'NullSource', '_ormbases': ['sitecontrol.CoreSource']},
            'coresource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sitecontrol.CoreSource']", 'unique': 'True', 'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {})
        },
        'sitecontrol.pagechecks': {
            'Meta': {'object_name': 'PageChecks'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'subsite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sitecontrol.CoreHost']"})
        },
        'sitecontrol.queuedupdate': {
            'Meta': {'object_name': 'QueuedUpdate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sitecontrol.CoreSite']"})
        }
    }

    complete_apps = ['sitecontrol']