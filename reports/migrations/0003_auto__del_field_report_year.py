# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Report.year'
        db.delete_column('reports_report', 'year')


    def backwards(self, orm):
        # Adding field 'Report.year'
        db.add_column('reports_report', 'year',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    models = {
        'reports.report': {
            'Meta': {'object_name': 'Report'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'horizontal': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'vertical': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['reports']