from django.contrib import admin
from models import (Topic, MarkdownElement, CodeElement, ImageElement,
                    AudioElement)

class MarkdownElementInline(admin.StackedInline):
    model = MarkdownElement

class CodeElementInline(admin.StackedInline):
    model = CodeElement

class ImageElementInline(admin.StackedInline):
    model = ImageElement

class AudioElementInline(admin.StackedInline):
    model = AudioElement

class TopicAdmin(admin.ModelAdmin):
    inlines = [
            MarkdownElementInline,
            CodeElementInline,
            ImageElementInline,
            AudioElementInline,
    ]

admin.site.register(Topic, TopicAdmin)
admin.site.register(MarkdownElement)
admin.site.register(CodeElement)
admin.site.register(ImageElement)
admin.site.register(AudioElement)
