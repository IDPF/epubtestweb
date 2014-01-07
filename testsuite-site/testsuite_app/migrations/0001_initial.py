# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Test'
        db.create_table('testsuite_app_test', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.Category'])),
            ('required', self.gf('django.db.models.fields.BooleanField')()),
            ('testid', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('testsuite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.TestSuite'])),
            ('xhtml', self.gf('django.db.models.fields.TextField')()),
            ('flagged_as_new', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flagged_as_changed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('testsuite_app', ['Test'])

        # Adding model 'Category'
        db.create_table('testsuite_app_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.Category'], null=True, blank=True)),
            ('testsuite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.TestSuite'])),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('testsuite_app', ['Category'])

        # Adding model 'Evaluation'
        db.create_table('testsuite_app_evaluation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testsuite', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.TestSuite'])),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('percent_complete', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('reading_system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.ReadingSystem'])),
            ('flagged_for_review', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('testsuite_app', ['Evaluation'])

        # Adding model 'ReadingSystem'
        db.create_table('testsuite_app_readingsystem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locale', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('operating_system', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sdk_version', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.UserProfile'])),
            ('visibility', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
        ))
        db.send_create_signal('testsuite_app', ['ReadingSystem'])

        # Adding model 'Result'
        db.create_table('testsuite_app_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('evaluation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.Evaluation'])),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.Test'])),
        ))
        db.send_create_signal('testsuite_app', ['Result'])

        # Adding model 'Score'
        db.create_table('testsuite_app_score', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_required_tests', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_optional_tests', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_required_passed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_optional_passed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pct_required_passed', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('pct_optional_passed', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('pct_total_passed', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2)),
            ('evaluation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.Evaluation'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testsuite_app.Category'], null=True, blank=True)),
        ))
        db.send_create_signal('testsuite_app', ['Score'])

        # Adding model 'TestSuite'
        db.create_table('testsuite_app_testsuite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version_date', self.gf('django.db.models.fields.DateField')(max_length=50)),
            ('version_revision', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('testsuite_app', ['TestSuite'])

        # Adding model 'UserProfile'
        db.create_table('testsuite_app_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('testsuite_app', ['UserProfile'])

        # Adding M2M table for field groups on 'UserProfile'
        m2m_table_name = db.shorten_name('testsuite_app_userprofile_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['testsuite_app.userprofile'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'UserProfile'
        m2m_table_name = db.shorten_name('testsuite_app_userprofile_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['testsuite_app.userprofile'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'permission_id'])


    def backwards(self, orm):
        # Deleting model 'Test'
        db.delete_table('testsuite_app_test')

        # Deleting model 'Category'
        db.delete_table('testsuite_app_category')

        # Deleting model 'Evaluation'
        db.delete_table('testsuite_app_evaluation')

        # Deleting model 'ReadingSystem'
        db.delete_table('testsuite_app_readingsystem')

        # Deleting model 'Result'
        db.delete_table('testsuite_app_result')

        # Deleting model 'Score'
        db.delete_table('testsuite_app_score')

        # Deleting model 'TestSuite'
        db.delete_table('testsuite_app_testsuite')

        # Deleting model 'UserProfile'
        db.delete_table('testsuite_app_userprofile')

        # Removing M2M table for field groups on 'UserProfile'
        db.delete_table(db.shorten_name('testsuite_app_userprofile_groups'))

        # Removing M2M table for field user_permissions on 'UserProfile'
        db.delete_table(db.shorten_name('testsuite_app_userprofile_user_permissions'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'testsuite_app.category': {
            'Meta': {'object_name': 'Category'},
            'category_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Category']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'testsuite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.TestSuite']"})
        },
        'testsuite_app.evaluation': {
            'Meta': {'object_name': 'Evaluation'},
            'flagged_for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'percent_complete': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'reading_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.ReadingSystem']"}),
            'testsuite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.TestSuite']"})
        },
        'testsuite_app.readingsystem': {
            'Meta': {'object_name': 'ReadingSystem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'operating_system': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sdk_version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.UserProfile']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visibility': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'})
        },
        'testsuite_app.result': {
            'Meta': {'object_name': 'Result'},
            'evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Evaluation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Test']"})
        },
        'testsuite_app.score': {
            'Meta': {'object_name': 'Score'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Category']", 'null': 'True', 'blank': 'True'}),
            'evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Evaluation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_optional_passed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_optional_tests': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_required_passed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_required_tests': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pct_optional_passed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'pct_required_passed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'pct_total_passed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'})
        },
        'testsuite_app.test': {
            'Meta': {'object_name': 'Test'},
            'depth': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'flagged_as_changed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flagged_as_new': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Category']"}),
            'required': ('django.db.models.fields.BooleanField', [], {}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'testid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'testsuite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.TestSuite']"}),
            'xhtml': ('django.db.models.fields.TextField', [], {})
        },
        'testsuite_app.testsuite': {
            'Meta': {'object_name': 'TestSuite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version_date': ('django.db.models.fields.DateField', [], {'max_length': '50'}),
            'version_revision': ('django.db.models.fields.IntegerField', [], {})
        },
        'testsuite_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['testsuite_app']