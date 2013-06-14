from django.db import models
from markdown import markdown
from model_utils.managers import InheritanceManager
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter

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

    # model_utils.managers.InheritanceManager allows us to fetch subclass
    # objects as instances of those subclasses rather than as instances of
    # BaseLessonElement. This means that the correct to_html() method will be
    # called in our views.
    objects = InheritanceManager()

    def to_html(self):
        raise NotImplementedError

    def __unicode__(self):
        return self.description

class MarkdownElement(BaseLessonElement):
    """
    A lesson element containing text written in the Markdown
    markup language.
    """

    text = models.TextField()

    def to_html(self):
        return markdown(self.text)

    class Meta:
        verbose_name = 'text element'

class CodeElement(BaseLessonElement):
    """
    A lesson element containing example code. The returned HTML is produced
    by Pygments attempting to guess the programming language and add markup
    for syntax highlighting.
    """

    code = models.TextField()

    def to_html(self):
        return highlight(self.code, guess_lexer(self.code), HtmlFormatter())

class Lesson(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title
