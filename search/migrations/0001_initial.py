# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SearchCategory'
        db.create_table('search_searchcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('search', ['SearchCategory'])


    def backwards(self, orm):
        
        # Deleting model 'SearchCategory'
        db.delete_table('search_searchcategory')


    models = {
        'search.searchcategory': {
            'Meta': {'object_name': 'SearchCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['search']
