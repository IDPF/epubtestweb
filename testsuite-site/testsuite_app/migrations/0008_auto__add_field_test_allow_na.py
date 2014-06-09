# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Test.allow_na'
        db.add_column('testsuite_app_test', 'allow_na',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Test.allow_na'
        db.delete_column('testsuite_app_test', 'allow_na')


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
        'testsuite_app.accessibilityscore': {
            'Meta': {'object_name': 'AccessibilityScore'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Category']", 'null': 'True', 'blank': 'True'}),
            'evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Evaluation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_applicable_tests': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_passed_tests': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pct_total_passed': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'result_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.ResultSet']", 'null': 'True', 'blank': 'True'})
        },
        'testsuite_app.category': {
            'Meta': {'object_name': 'Category'},
            'category_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Category']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'temp_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'testsuite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.TestSuite']"})
        },
        'testsuite_app.evaluation': {
            'Meta': {'object_name': 'Evaluation'},
            'accessibility_testsuite': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'evaluation_accessibility_testsuite'", 'null': 'True', 'to': "orm['testsuite_app.TestSuite']"}),
            'flagged_for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'percent_complete': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'reading_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.ReadingSystem']"}),
            'testsuite': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'evaluation_testsuite'", 'to': "orm['testsuite_app.TestSuite']"})
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
            'publish_notes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'result_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.ResultSet']", 'null': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Test']"})
        },
        'testsuite_app.resultset': {
            'Meta': {'object_name': 'ResultSet', 'db_table': "'testsuite_app_result_set'"},
            'evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Evaluation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.ResultSetMetadata']", 'null': 'True', 'blank': 'True'}),
            'percent_complete': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'testsuite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.TestSuite']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        'testsuite_app.resultsetmetadata': {
            'Meta': {'object_name': 'ResultSetMetadata', 'db_table': "'testsuite_app_result_set_metadata'"},
            'assistive_technology': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_braille': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_keyboard': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_mouse': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_screenreader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_touch': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'allow_na': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'testsuite_app.testmetadata': {
            'Meta': {'object_name': 'TestMetadata', 'db_table': "'testsuite_app_test_metadata'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_advanced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testsuite_app.Test']"})
        },
        'testsuite_app.testsuite': {
            'Meta': {'object_name': 'TestSuite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'testsuite_type': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
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