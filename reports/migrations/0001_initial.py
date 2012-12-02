# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Report'
        db.create_table('reports_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('horizontal', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('vertical', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('time_range', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('reports', ['Report'])


    def backwards(self, orm):
        # Deleting model 'Report'
        db.delete_table('reports_report')


    models = {
        'reports.report': {
            'Meta': {'object_name': 'Report'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'horizontal': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'time_range': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'vertical': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['reports']