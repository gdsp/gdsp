from django.contrib import admin
from models import Lesson, MarkdownElement

class MarkdownElementInline(admin.StackedInline):
    model = MarkdownElement

class LessonAdmin(admin.ModelAdmin):
    inlines = [MarkdownElementInline]

admin.site.register(Lesson, LessonAdmin)
admin.site.register(MarkdownElement)
