# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Permission'
        db.create_table('auth_permission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('auth', ['Permission'])

        # Adding unique constraint on 'Permission', fields ['content_type', 'codename']
        db.create_unique('auth_permission', ['content_type_id', 'codename'])

        # Adding model 'Group'
        db.create_table('auth_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal('auth', ['Group'])

        # Adding M2M table for field permissions on 'Group'
        db.create_table('auth_group_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['auth.group'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique('auth_group_permissions', ['group_id', 'permission_id'])

        # Adding model 'User'
        db.create_table('auth_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('auth', ['User'])

        # Adding M2M table for field groups on 'User'
        db.create_table('auth_user_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['auth.user'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('auth_user_groups', ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        db.create_table('auth_user_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['auth.user'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique('auth_user_user_permissions', ['user_id', 'permission_id'])

        # Adding model 'Employee'
        db.create_table('auth_employee', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('patronymic', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('auth', ['Employee'])

        # Adding M2M table for field department on 'Employee'
        db.create_table('auth_employee_department', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employee', models.ForeignKey(orm['auth.employee'], null=False)),
            ('department', models.ForeignKey(orm['core.department'], null=False))
        ))
        db.create_unique('auth_employee_department', ['employee_id', 'department_id'])

        # Adding model 'Listener'
        db.create_table('auth_listener', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('patronymic', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Organization'])),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('profile', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('first_name_inflated', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name_inflated', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('patronymic_inflated', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('auth', ['Listener'])


    def backwards(self, orm):
        # Removing unique constraint on 'Permission', fields ['content_type', 'codename']
        db.delete_unique('auth_permission', ['content_type_id', 'codename'])

        # Deleting model 'Permission'
        db.delete_table('auth_permission')

        # Deleting model 'Group'
        db.delete_table('auth_group')

        # Removing M2M table for field permissions on 'Group'
        db.delete_table('auth_group_permissions')

        # Deleting model 'User'
        db.delete_table('auth_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table('auth_user_groups')

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table('auth_user_user_permissions')

        # Deleting model 'Employee'
        db.delete_table('auth_employee')

        # Removing M2M table for field department on 'Employee'
        db.delete_table('auth_employee_department')

        # Deleting model 'Listener'
        db.delete_table('auth_listener')


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
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name_inflated': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'last_name_inflated': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Organization']"}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'patronymic_inflated': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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