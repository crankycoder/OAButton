# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'OADocument'
        db.delete_table(u'api_oadocument')

        # Adding model 'PendingOpen'
        db.create_table(u'api_pendingopen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender_email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('subject', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('email_text', self.gf('django.db.models.fields.TextField')(max_length=4000)),
        ))
        db.send_create_signal(u'api', ['PendingOpen'])

        # Adding model 'OpenDocument'
        db.create_table(u'api_opendocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doi', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('oa_url', self.gf('django.db.models.fields.URLField')(max_length=2000)),
            ('primary_author_email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('date_opened', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'api', ['OpenDocument'])


    def backwards(self, orm):
        # Adding model 'OADocument'
        db.create_table(u'api_oadocument', (
            ('doi', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('primary_author_email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('oa_url', self.gf('django.db.models.fields.URLField')(max_length=2000)),
            ('date_opened', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'api', ['OADocument'])

        # Deleting model 'PendingOpen'
        db.delete_table(u'api_pendingopen')

        # Deleting model 'OpenDocument'
        db.delete_table(u'api_opendocument')


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
        u'api.opendocument': {
            'Meta': {'object_name': 'OpenDocument'},
            'date_opened': ('django.db.models.fields.DateTimeField', [], {}),
            'doi': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oa_url': ('django.db.models.fields.URLField', [], {'max_length': '2000'}),
            'primary_author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'})
        },
        u'api.pendingopen': {
            'Meta': {'object_name': 'PendingOpen'},
            'email_text': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'max_length': '2000'})
        }
    }

    complete_apps = ['api']