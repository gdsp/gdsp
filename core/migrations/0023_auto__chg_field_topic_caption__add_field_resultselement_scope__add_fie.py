# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Topic.caption'
        db.alter_column(u'core_topic', 'caption', self.gf('django.db.models.fields.CharField')(max_length=255))
        # Adding field 'ResultsElement.scope'
        db.add_column(u'core_resultselement', 'scope',
                      self.gf('django.db.models.fields.CharField')(default='Lesson', max_length=256),
                      keep_default=False)

        # Adding field 'TestElement.feedback_bad'
        db.add_column(u'core_testelement', 'feedback_bad',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'TestElement.feecback_ok'
        db.add_column(u'core_testelement', 'feecback_ok',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'TestElement.feecback_good'
        db.add_column(u'core_testelement', 'feecback_good',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Topic.caption'
        db.alter_column(u'core_topic', 'caption', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))
        # Deleting field 'ResultsElement.scope'
        db.delete_column(u'core_resultselement', 'scope')

        # Deleting field 'TestElement.feedback_bad'
        db.delete_column(u'core_testelement', 'feedback_bad')

        # Deleting field 'TestElement.feecback_ok'
        db.delete_column(u'core_testelement', 'feecback_ok')

        # Deleting field 'TestElement.feecback_good'
        db.delete_column(u'core_testelement', 'feecback_good')


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
            'hover': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        u'core.basetopicelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'BaseTopicElement'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['core.Topic']"})
        },
        u'core.codeelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'CodeElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {})
        },
        u'core.course': {
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.imageelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ImageElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'max_width': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        },
        u'core.lesson': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Lesson'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lessons'", 'to': u"orm['core.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'no-img.jpg'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Topic']", 'through': u"orm['core.LessonTopicRelation']", 'symmetrical': 'False'})
        },
        u'core.lessontopicrelation': {
            'Meta': {'ordering': "['lesson', 'topic_ordinal']", 'object_name': 'LessonTopicRelation', 'index_together': "[['lesson', 'topic_ordinal']]"},
            'excluded_content': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Lesson']"}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Topic']"}),
            'topic_ordinal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
        u'core.mathelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'MathElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'latex': ('django.db.models.fields.TextField', [], {})
        },
        u'core.resultselement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'ResultsElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'scope': ('django.db.models.fields.CharField', [], {'default': "'Lesson'", 'max_length': '256'})
        },
        u'core.testelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'TestElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'difficulty': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'effect_files': ('core.multiple.MultiSelectField', [], {'default': "'NULL.inc'", 'max_length': '10000'}),
            'feecback_good': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'feecback_ok': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'feedback_bad': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'core.topic': {
            'Meta': {'ordering': "['lessontopicrelation__lesson', 'lessontopicrelation__topic_ordinal']", 'object_name': 'Topic'},
            'caption': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']