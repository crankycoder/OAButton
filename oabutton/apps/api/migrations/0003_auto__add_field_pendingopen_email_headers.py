# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PendingOpen.email_headers'
        db.add_column(u'api_pendingopen', 'email_headers',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=4000),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PendingOpen.email_headers'
        db.delete_column(u'api_pendingopen', 'email_headers')


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
            'email_headers': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '4000'}),
            'email_text': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'max_length': '2000'})
        }
    }

    complete_apps = ['api']