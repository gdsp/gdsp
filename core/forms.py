from django import forms

from models import Lesson, BaseTopicElement

# The CSV handling code in this file draws heavily from this snippet:
#   http://djangosnippets.org/snippets/2860/

class CSVCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    def value_from_datadict(self, data, files, name):
        # The database expects a string (of CSV), so let's give it one.
        return ','.join(data.getlist(name))

    def render(self, name, value, attrs=None, choices=()):
        # The checkbox rendering code expects a list, not a string;
        # let's give it one.
        if value:
            value = value.split(',')
        return super(CSVCheckboxSelectMultiple, self).render(name, value,
                                                             attrs=attrs,
                                                             choices=choices)


class CSVMultipleChoiceField(forms.MultipleChoiceField):
    widget = CSVCheckboxSelectMultiple

    def to_python(self, value):
        # We want to store the value as it is, a string of CSV,
        # and not convert it to a list.
        return value

    def validate(self, value):
        # The MultipleChoiceField validator expects a list.
        if value:
            value = value.split(',')
        super(CSVMultipleChoiceField, self).validate(value)


class TopicInlineForm(forms.ModelForm):
    excluded_content = CSVMultipleChoiceField(
            choices=BaseTopicElement.ELEMENT_TYPES,
            required=False,
            label='Excluded content',
    )

    class Meta:
        model = Lesson.topics.through
        fields = ['topic_ordinal', 'topic', 'excluded_content']
