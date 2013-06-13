from django.db import models

class BaseLessonElement(models.Model):
    """
    A base class for the elements that go into a lesson, such as
    text, images etc. The description attribute should describe to an
    administrator putting together a lesson what the subject matter
    of the element is.

    Inheriting classes must implement a to_html() instance method
    which renders an HTML representation of the element suitable to be
    included as part of a web page.
    """

    description = models.CharField(max_length=255)
    lesson = models.ForeignKey('Lesson', related_name='elements')

    def to_html(self):
        raise NotImplementedError

    def __unicode__(self):
        return self.description

class Lesson(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title
