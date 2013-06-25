# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LowerCaseTaggedItem'
        db.create_table(u'core_lowercasetaggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'core_lowercasetaggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tagged_items', to=orm['core.LowerCaseTag'])),
        ))
        db.send_create_signal(u'core', ['LowerCaseTaggedItem'])

        # Adding model 'LowerCaseTag'
        db.create_table(u'core_lowercasetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'core', ['LowerCaseTag'])


    def backwards(self, orm):
        # Deleting model 'LowerCaseTaggedItem'
        db.delete_table(u'core_lowercasetaggeditem')

        # Deleting model 'LowerCaseTag'
        db.delete_table(u'core_lowercasetag')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.audioelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'AudioElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.basetopicelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'BaseTopicElement'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['core.Topic']"})
        },
        u'core.codeelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'CodeElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {})
        },
        u'core.imageelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ImageElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.lowercasetag': {
            'Meta': {'object_name': 'LowerCaseTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.lowercasetaggeditem': {
            'Meta': {'object_name': 'LowerCaseTaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'core_lowercasetaggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tagged_items'", 'to': u"orm['core.LowerCaseTag']"})
        },
        u'core.markdownelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'MarkdownElement', '_ormbases': [u'core.BaseTopicElement']},
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