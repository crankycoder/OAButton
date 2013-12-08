# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OAApiKey'
        db.create_table(u'api_oaapikey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner_email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('api_key', self.gf('django.db.models.fields.TextField')(max_length=40)),
            ('date_requested', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('verification_secret', self.gf('django.db.models.fields.TextField')(max_length=40)),
            ('date_enabled', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'api', ['OAApiKey'])

        # Adding model 'OADocument'
        db.create_table(u'api_oadocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doi', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('oa_url', self.gf('django.db.models.fields.URLField')(max_length=2000)),
            ('primary_author_email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('date_opened', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'api', ['OADocument'])


    def backwards(self, orm):
        # Deleting model 'OAApiKey'
        db.delete_table(u'api_oaapikey')

        # Deleting model 'OADocument'
        db.delete_table(u'api_oadocument')


    models = {
        u'api.oaapikey': {
            'Meta': {'object_name': 'OAApiKey'},
            'api_key': ('django.db.models.fields.TextField', [], {'max_length': '40'}),
            'date_enabled': ('django.db.models.fields.DateTimeField', [], {}),
            'date_requested': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'verification_secret': ('django.db.models.fields.TextField', [], {'max_length': '40'})
        },
        u'api.oadocument': {
            'Meta': {'object_name': 'OADocument'},
            'date_opened': ('django.db.models.fields.DateTimeField', [], {}),
            'doi': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oa_url': ('django.db.models.fields.URLField', [], {'max_length': '2000'}),
            'primary_author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'})
        }
    }

    complete_apps = ['api']