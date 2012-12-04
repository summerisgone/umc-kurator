# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Listener.category'
        db.alter_column('auth_listener', 'category', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Listener.profile'
        db.alter_column('auth_listener', 'profile', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Listener.patronymic_inflated'
        db.alter_column('auth_listener', 'patronymic_inflated', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Listener.first_name_inflated'
        db.alter_column('auth_listener', 'first_name_inflated', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Listener.position'
        db.alter_column('auth_listener', 'position', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Listener.last_name_inflated'
        db.alter_column('auth_listener', 'last_name_inflated', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'Listener.category'
        db.alter_column('auth_listener', 'category', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Listener.profile'
        db.alter_column('auth_listener', 'profile', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Listener.patronymic_inflated'
        db.alter_column('auth_listener', 'patronymic_inflated', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Listener.first_name_inflated'
        db.alter_column('auth_listener', 'first_name_inflated', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Listener.position'
        db.alter_column('auth_listener', 'position', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Listener.last_name_inflated'
        db.alter_column('auth_listener', 'last_name_inflated', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        'auth.employee': {
            'Meta': {'object_name': 'Employee'},
            'department': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Department']", 'symmetrical': 'False'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.listener': {
            'Meta': {'object_name': 'Listener'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name_inflated': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_name_inflated': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Organization']"}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'patronymic_inflated': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.department': {
            'Meta': {'object_name': 'Department'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.organization': {
            'Meta': {'object_name': 'Organization'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cast': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['auth']