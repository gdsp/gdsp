# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Renaming model 'BaseLessonElement'
        db.rename_table(u'core_baselessonelement', u'core_basetopicelement')
        db.send_create_signal(u'core', ['BaseTopicElement'])

        # Renaming model 'Lesson'
        db.rename_table(u'core_lesson', u'core_topic')
        db.send_create_signal(u'core', ['Topic'])

        # Renaming field 'ImageElement.baselessonelement_ptr'
        db.rename_column(u'core_imageelement', u'baselessonelement_ptr_id', u'basetopicelement_ptr_id')

        # Renaming field 'CodeElement.baselessonelement_ptr'
        db.rename_column(u'core_codeelement', u'baselessonelement_ptr_id', u'basetopicelement_ptr_id')

        # Renaming field 'MarkdownElement.baselessonelement_ptr'
        db.rename_column(u'core_markdownelement', u'baselessonelement_ptr_id', u'basetopicelement_ptr_id')

        # Renaming field 'BaseLessonElement.lesson_id'
        db.rename_column(u'core_basetopicelement', u'lesson_id', u'topic_id')

    def backwards(self, orm):
        # Renaming model 'BaseTopicElement'
        db.rename_table(u'core_basetopicelement', u'core_baselessonelement')
        db.send_create_signal(u'core', ['BaseLessonElement'])

        # Renaming model 'Topic'
        db.rename_table(u'core_topic', u'core_lesson')
        db.send_create_signal(u'core', ['Lesson'])

        # Renaming field 'ImageElement.basetopicelement_ptr'
        db.rename_column(u'core_imageelement', u'basetopicelement_ptr_id', u'baselessonelement_ptr_id')

        # Renaming field 'CodeElement.basetopicelement_ptr'
        db.rename_column(u'core_codeelement', u'basetopicelement_ptr_id', u'baselessonelement_ptr_id')

        # Renaming field 'MarkdownElement.basetopicelement_ptr'
        db.rename_column(u'core_markdownelement', u'basetopicelement_ptr_id', u'baselessonelement_ptr_id')

        # Renaming field 'BaseTopicElement.lesson_id'
        db.rename_column(u'core_baselessonelement', u'topic_id', u'lesson_id')

    models = {
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
