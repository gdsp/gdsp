from django.contrib import admin
from models import Lesson, MarkdownElement, CodeElement, ImageElement

class MarkdownElementInline(admin.StackedInline):
    model = MarkdownElement

class CodeElementInline(admin.StackedInline):
    model = CodeElement

class ImageElementInline(admin.StackedInline):
    model = ImageElement

class LessonAdmin(admin.ModelAdmin):
    inlines = [
            MarkdownElementInline,
            CodeElementInline,
            ImageElementInline,
    ]

admin.site.register(Lesson, LessonAdmin)
admin.site.register(MarkdownElement)
admin.site.register(CodeElement)
admin.site.register(ImageElement)
