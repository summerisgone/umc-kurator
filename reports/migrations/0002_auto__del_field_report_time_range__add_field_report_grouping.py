# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Report.time_range'
        db.delete_column('reports_report', 'time_range')

        # Adding field 'Report.grouping'
        db.add_column('reports_report', 'grouping',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Report.time_range'
        db.add_column('reports_report', 'time_range',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)

        # Deleting field 'Report.grouping'
        db.delete_column('reports_report', 'grouping')


    models = {
        'reports.report': {
            'Meta': {'object_name': 'Report'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'horizontal': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'vertical': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['reports']