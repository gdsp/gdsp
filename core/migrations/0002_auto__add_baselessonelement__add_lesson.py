# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BaseLessonElement'
        db.create_table(u'core_baselessonelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(related_name='elements', to=orm['core.Lesson'])),
        ))
        db.send_create_signal(u'core', ['BaseLessonElement'])

        # Adding model 'Lesson'
        db.create_table(u'core_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['Lesson'])


    def backwards(self, orm):
        # Deleting model 'BaseLessonElement'
        db.delete_table(u'core_baselessonelement')

        # Deleting model 'Lesson'
        db.delete_table(u'core_lesson')


    models = {
        u'core.baselessonelement': {
            'Meta': {'object_name': 'BaseLessonElement'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['core.Lesson']"})
        },
        u'core.lesson': {
            'Meta': {'object_name': 'Lesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']