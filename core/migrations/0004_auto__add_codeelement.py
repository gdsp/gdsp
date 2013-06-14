# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CodeElement'
        db.create_table(u'core_codeelement', (
            (u'baselessonelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseLessonElement'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['CodeElement'])


    def backwards(self, orm):
        # Deleting model 'CodeElement'
        db.delete_table(u'core_codeelement')


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