# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Report.created'
        db.add_column('reports_report', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 12, 4, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Report.created'
        db.delete_column('reports_report', 'created')


    models = {
        'reports.report': {
            'Meta': {'object_name': 'Report'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'filter_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'filter_value': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'horizontal': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report_name': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'vertical': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['reports']