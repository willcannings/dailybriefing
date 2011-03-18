# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Page.analysis_delta'
        db.add_column('search_page', 'analysis_delta', self.gf('django.db.models.fields.IntegerField')(default=60), keep_default=False)

        # Changing field 'Page.next_analysis'
        db.alter_column('search_page', 'next_analysis', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, default=datetime.datetime(2011, 3, 16, 10, 51, 37, 561984)))

        # Changing field 'Page.first_analysed'
        db.alter_column('search_page', 'first_analysed', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Page.last_analysed'
        db.alter_column('search_page', 'last_analysed', self.gf('django.db.models.fields.DateTimeField')(null=True))


    def backwards(self, orm):
        
        # Deleting field 'Page.analysis_delta'
        db.delete_column('search_page', 'analysis_delta')

        # Changing field 'Page.next_analysis'
        db.alter_column('search_page', 'next_analysis', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # User chose to not deal with backwards NULL issues for 'Page.first_analysed'
        raise RuntimeError("Cannot reverse this migration. 'Page.first_analysed' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Page.last_analysed'
        raise RuntimeError("Cannot reverse this migration. 'Page.last_analysed' and its values cannot be restored.")


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'blank': 'True'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'search.link': {
            'Meta': {'object_name': 'Link'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outbound': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inbound_set'", 'to': "orm['search.Page']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outbound_set'", 'to': "orm['search.Page']"})
        },
        'search.newssource': {
            'Meta': {'object_name': 'NewsSource'},
            'a1': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'a2': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'delayed_ready': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'delayed_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l1': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'l2': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'last_24_hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_hour': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_pages': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'queue_immediate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            't1': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            't2': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'total_indexed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url_wildcard': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'search.page': {
            'Meta': {'object_name': 'Page'},
            'analysis_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'analysis_delta': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'first_analysed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_analysed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'news_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.NewsSource']"}),
            'next_analysis': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_on_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'times_changed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'search.searchcategory': {
            'Meta': {'object_name': 'SearchCategory'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'search.searchitem': {
            'Meta': {'object_name': 'SearchItem'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.SearchCategory']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['search']
