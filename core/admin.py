from django.contrib import admin
from forms import TopicInlineForm
from models import (Course, Lesson, Topic, BaseTopicElement, MarkdownElement,
                    CodeElement, ImageElement, AudioElement, MathElement, TestElement, ResultsElement)

class BaseTopicElementInline(admin.StackedInline):
    model = BaseTopicElement
    template = 'admin/core/inline_basetopicelement.html'
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


class MathElementInline(admin.StackedInline):
    model = MathElement
    extra = 0


class TestElementInline(admin.StackedInline):
    model = TestElement
    extra = 0


class ResultsElementInline(admin.StackedInline):
    model = ResultsElement
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    inlines = [
            BaseTopicElementInline,
            MarkdownElementInline,
            CodeElementInline,
            ImageElementInline,
            AudioElementInline,
            MathElementInline,
            TestElementInline,
            ResultsElementInline,
    ]
    search_fields = ['title', 'tags__name']

    class Media:
        js = ['javascript/autocomplete-topic-tags.js']

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
        formset.save_m2m()


class TopicInline(admin.TabularInline):
    model = Lesson.topics.through
    form = TopicInlineForm
    template = 'admin/core/inline_topic.html'
    raw_id_fields = ['topic']
    extra = 0


class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    inlines = [TopicInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    ordering = ['_order']


class CourseAdmin(admin.ModelAdmin):
    model = Course
    inlines = [LessonInline]


admin.site.register(Topic, TopicAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Course, CourseAdmin)
