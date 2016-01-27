# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BaseTopicElement'
        db.create_table(u'core_basetopicelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='elements', to=orm['core.Topic'])),
            ('element_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['BaseTopicElement'])

        # Adding model 'MarkdownElement'
        db.create_table(u'core_markdownelement', (
            (u'basetopicelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseTopicElement'], unique=True, primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['MarkdownElement'])

        # Adding model 'CodeElement'
        db.create_table(u'core_codeelement', (
            (u'basetopicelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseTopicElement'], unique=True, primary_key=True)),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['CodeElement'])

        # Adding model 'ImageElement'
        db.create_table(u'core_imageelement', (
            (u'basetopicelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseTopicElement'], unique=True, primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('max_width', self.gf('django.db.models.fields.IntegerField')(default=100)),
        ))
        db.send_create_signal(u'core', ['ImageElement'])

        # Adding model 'AudioElement'
        db.create_table(u'core_audioelement', (
            (u'basetopicelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseTopicElement'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('hover', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['AudioElement'])

        # Adding model 'TestElement'
        db.create_table(u'core_testelement', (
            (u'basetopicelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseTopicElement'], unique=True, primary_key=True)),
            ('test', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('difficulty', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('effect_files', self.gf('core.multiple.MultiSelectField')(default='NULL.inc', max_length=10000)),
            ('feedback_bad', self.gf('django.db.models.fields.TextField')()),
            ('feecback_ok', self.gf('django.db.models.fields.TextField')()),
            ('feecback_good', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['TestElement'])

        # Adding model 'ResultsElement'
        db.create_table(u'core_resultselement', (
            (u'basetopicelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseTopicElement'], unique=True, primary_key=True)),
            ('scope', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'core', ['ResultsElement'])

        # Adding model 'MathElement'
        db.create_table(u'core_mathelement', (
            (u'basetopicelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseTopicElement'], unique=True, primary_key=True)),
            ('latex', self.gf('django.db.models.fields.TextField')()),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['MathElement'])

        # Adding model 'LowerCaseTag'
        db.create_table(u'core_lowercasetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'core', ['LowerCaseTag'])

        # Adding model 'LowerCaseTaggedItem'
        db.create_table(u'core_lowercasetaggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'core_lowercasetaggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tagged_items', to=orm['core.LowerCaseTag'])),
        ))
        db.send_create_signal(u'core', ['LowerCaseTaggedItem'])

        # Adding model 'Topic'
        db.create_table(u'core_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('caption', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['Topic'])

        # Adding model 'Lesson'
        db.create_table(u'core_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='no-img.jpg', max_length=100)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lessons', to=orm['core.Course'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['Lesson'])

        # Adding model 'LessonTopicRelation'
        db.create_table(u'core_lessontopicrelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Topic'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Lesson'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('topic_ordinal', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('excluded_content', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['LessonTopicRelation'])

        # Adding index on 'LessonTopicRelation', fields ['lesson', 'topic_ordinal']
        db.create_index(u'core_lessontopicrelation', ['lesson_id', 'topic_ordinal'])

        # Adding model 'Course'
        db.create_table(u'core_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['Course'])


    def backwards(self, orm):
        # Removing index on 'LessonTopicRelation', fields ['lesson', 'topic_ordinal']
        db.delete_index(u'core_lessontopicrelation', ['lesson_id', 'topic_ordinal'])

        # Deleting model 'BaseTopicElement'
        db.delete_table(u'core_basetopicelement')

        # Deleting model 'MarkdownElement'
        db.delete_table(u'core_markdownelement')

        # Deleting model 'CodeElement'
        db.delete_table(u'core_codeelement')

        # Deleting model 'ImageElement'
        db.delete_table(u'core_imageelement')

        # Deleting model 'AudioElement'
        db.delete_table(u'core_audioelement')

        # Deleting model 'TestElement'
        db.delete_table(u'core_testelement')

        # Deleting model 'ResultsElement'
        db.delete_table(u'core_resultselement')

        # Deleting model 'MathElement'
        db.delete_table(u'core_mathelement')

        # Deleting model 'LowerCaseTag'
        db.delete_table(u'core_lowercasetag')

        # Deleting model 'LowerCaseTaggedItem'
        db.delete_table(u'core_lowercasetaggeditem')

        # Deleting model 'Topic'
        db.delete_table(u'core_topic')

        # Deleting model 'Lesson'
        db.delete_table(u'core_lesson')

        # Deleting model 'LessonTopicRelation'
        db.delete_table(u'core_lessontopicrelation')

        # Deleting model 'Course'
        db.delete_table(u'core_course')


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
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'core.testelement': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'TestElement', '_ormbases': [u'core.BaseTopicElement']},
            u'basetopicelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.BaseTopicElement']", 'unique': 'True', 'primary_key': 'True'}),
            'difficulty': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'effect_files': ('core.multiple.MultiSelectField', [], {'default': "'NULL.inc'", 'max_length': '10000'}),
            'feecback_good': ('django.db.models.fields.TextField', [], {}),
            'feecback_ok': ('django.db.models.fields.TextField', [], {}),
            'feedback_bad': ('django.db.models.fields.TextField', [], {}),
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