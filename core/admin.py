from django.contrib import admin
from models import (Topic, BaseTopicElement, MarkdownElement, CodeElement,
                    ImageElement, AudioElement)

class BaseTopicElementInline(admin.StackedInline):
    model = BaseTopicElement
    template = 'admin/core/topic/inline_basetopicelement.html'
    ordering = ['_order']
    readonly_fields = ['description']
    max_num = 0

    def get_formset(self, request, obj=None, **kwargs):
        kwargs.update({'can_order': True, 'can_delete': False})
        return super(BaseTopicElementInline, self).get_formset(request, obj,
                                                               **kwargs)


class MarkdownElementInline(admin.StackedInline):
    model = MarkdownElement
    extra = 0


class CodeElementInline(admin.StackedInline):
    model = CodeElement
    extra = 0


class ImageElementInline(admin.StackedInline):
    model = ImageElement
    extra = 0


class AudioElementInline(admin.StackedInline):
    model = AudioElement
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    inlines = [
            BaseTopicElementInline,
            MarkdownElementInline,
            CodeElementInline,
            ImageElementInline,
            AudioElementInline,
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        if hasattr(formset, 'ordered_forms'):
            for form in formset.ordered_forms:
                # The _order field is 0-indexed, whereas the form's 'ORDER'
                # values are 1-indexed, hence the subtraction.
                form.instance._order = form.cleaned_data['ORDER'] - 1
                form.instance.save()
        else:
            for instance in instances:
                instance.save()
        # We don't actually have any many-to-many fields at the time
        # of writing, but you never know what the future will bring.
        formset.save_m2m()


admin.site.register(Topic, TopicAdmin)
admin.site.register(MarkdownElement)
admin.site.register(CodeElement)
admin.site.register(ImageElement)
admin.site.register(AudioElement)
