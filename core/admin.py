from django.contrib import admin
from models import Lesson, MarkdownElement, CodeElement

class MarkdownElementInline(admin.StackedInline):
    model = MarkdownElement

class CodeElementInline(admin.StackedInline):
    model = CodeElement

class LessonAdmin(admin.ModelAdmin):
    inlines = [MarkdownElementInline, CodeElementInline]

admin.site.register(Lesson, LessonAdmin)
admin.site.register(MarkdownElement)
admin.site.register(CodeElement)
