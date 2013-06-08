# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CoreSource'
        db.create_table('sitecontrol_coresource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('sitecontrol', ['CoreSource'])

        # Adding model 'CoreSite'
        db.create_table('sitecontrol_coresite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('root', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitecontrol.CoreSource'])),
        ))
        db.send_create_signal('sitecontrol', ['CoreSite'])

        # Adding model 'GitSource'
        db.create_table('sitecontrol_gitsource', (
            ('coresource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sitecontrol.CoreSource'], unique=True, primary_key=True)),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('poll_period_minutes', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('sitecontrol', ['GitSource'])

        # Adding model 'NullSource'
        db.create_table('sitecontrol_nullsource', (
            ('coresource_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sitecontrol.CoreSource'], unique=True, primary_key=True)),
            ('reason', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sitecontrol', ['NullSource'])

        # Adding model 'DeployCommand'
        db.create_table('sitecontrol_deploycommand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitecontrol.CoreSite'])),
            ('program', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('arguments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sitecontrol', ['DeployCommand'])


    def backwards(self, orm):
        # Deleting model 'CoreSource'
        db.delete_table('sitecontrol_coresource')

        # Deleting model 'CoreSite'
        db.delete_table('sitecontrol_coresite')

        # Deleting model 'GitSource'
        db.delete_table('sitecontrol_gitsource')

        # Deleting model 'NullSource'
        db.delete_table('sitecontrol_nullsource')

        # Deleting model 'DeployCommand'
        db.delete_table('sitecontrol_deploycommand')


    models = {
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
        }
    }

    complete_apps = ['sitecontrol']