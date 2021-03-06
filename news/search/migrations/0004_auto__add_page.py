# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('search_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('news_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.NewsSource'])),
            ('html', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('first_analysed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_analysed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('next_analysis', self.gf('django.db.models.fields.DateTimeField')()),
            ('analysis_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('times_changed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('time_on_index', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('search', ['Page'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('search_page')


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
        'search.newsindexpage': {
            'Meta': {'object_name': 'NewsIndexPage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.NewsSource']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'first_analysed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_analysed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'news_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['search.NewsSource']"}),
            'next_analysis': ('django.db.models.fields.DateTimeField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'time_on_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'times_changed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'search.searchcategory': {
            'Meta': {'object_name': 'SearchCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
