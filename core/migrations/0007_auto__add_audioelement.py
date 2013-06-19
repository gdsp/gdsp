# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AudioElement'
        db.create_table(u'core_audioelement', (
            (u'basetopicelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseTopicElement'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['AudioElement'])


    def backwards(self, orm):
        # Deleting model 'AudioElement'
        db.delete_table(u'core_audioelement')


    models = {
        u'core.audioelement': {
            'Meta': {'object_name': 'AudioElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.basetopicelement': {
            'Meta': {'object_name': 'BaseTopicElement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['core.Topic']"})
        },
        u'core.codeelement': {
            'Meta': {'object_name': 'CodeElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {})
        },
        u'core.imageelement': {
            'Meta': {'object_name': 'ImageElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.markdownelement': {
            'Meta': {'object_name': 'MarkdownElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'core.topic': {
            'Meta': {'object_name': 'Topic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']