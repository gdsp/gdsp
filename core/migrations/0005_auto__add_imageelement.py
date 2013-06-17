# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImageElement'
        db.create_table(u'core_imageelement', (
            (u'baselessonelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseLessonElement'], unique=True, primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['ImageElement'])


    def backwards(self, orm):
        # Deleting model 'ImageElement'
        db.delete_table(u'core_imageelement')


    models = {
        u'core.baselessonelement': {
            'Meta': {'object_name': 'BaseLessonElement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['core.Lesson']"})
        },
        u'core.codeelement': {
            'Meta': {'object_name': 'CodeElement', '_ormbases': [u'core.BaseLessonElement']},
            u'baselessonelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseLessonElement']", 'unique': 'True', 'primary_key': 'True'}),
            'code': ('django.db.models.fields.TextField', [], {})
        },
        u'core.imageelement': {
            'Meta': {'object_name': 'ImageElement', '_ormbases': [u'core.BaseLessonElement']},
            u'baselessonelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseLessonElement']", 'unique': 'True', 'primary_key': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.lesson': {
            'Meta': {'object_name': 'Lesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.markdownelement': {
            'Meta': {'object_name': 'MarkdownElement', '_ormbases': [u'core.BaseLessonElement']},
            u'baselessonelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseLessonElement']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']