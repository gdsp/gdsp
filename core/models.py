from django.db import models
from markdown import markdown
from model_utils.managers import InheritanceManager
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter

class BaseTopicElement(models.Model):
    """
    A base class for the elements that go into a topic, such as text,
    images etc. The description attribute should describe to an
    administrator putting together a topic what the subject matter of
    the element is.

    Inheriting classes must implement a to_html() instance method
    which renders an HTML representation of the element suitable to be
    included as part of a web page.
    """

    description = models.CharField(
            max_length=255,
            help_text='What does this element contain?',
    )
    topic = models.ForeignKey('Topic', related_name='elements')

    # model_utils.managers.InheritanceManager allows us to fetch subclass
    # objects as instances of those subclasses rather than as instances of
    # BaseTopicElement. This means that the correct to_html() method will be
    # called in our views.
    objects = InheritanceManager()

    def to_html(self):
        raise NotImplementedError

    def __unicode__(self):
        return self.description

class MarkdownElement(BaseTopicElement):
    """
    A topic element containing text written in the Markdown
    markup language.
    """

    text = models.TextField()

    def to_html(self):
        return markdown(self.text)

    class Meta:
        verbose_name = 'text element'

class CodeElement(BaseTopicElement):
    """
    A topic element containing example code. Its HTML representation is
    produced by Pygments attempting to guess the programming language and
    add markup for syntax highlighting.
    """

    code = models.TextField()

    def to_html(self):
        return highlight(self.code, guess_lexer(self.code), HtmlFormatter())

class ImageElement(BaseTopicElement):
    """
    A topic element containing an image and, optionally, a caption.
    Its  HTML representation wraps the image and caption (if present)
    in a figure element.
    """

    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='images')

    def to_html(self):
        html = u'<figure class="image-element">'
        html += u'<img src="{}">'.format(self.image.url)
        if self.caption:
            html += u'<figcaption>{}</figcaption>'.format(self.caption)
        html += u'</figure>'
        return html

class AudioElement(BaseTopicElement):
    """
    A topic element containing an audio file and a title. Its HTML
    representation is a link which, if all goes well, plays / stops
    the audio when clicked; if a problem occurs, it falls back to
    being a regular link allowing the student to download the file.
    """

    title = models.CharField(
            max_length=128,
            help_text='The title of the track as displayed to the student.',
    )
    file = models.FileField(upload_to='audio')

    def to_html(self):
        return u'<a class="audio-element" href="{url}">{title}</a>'.format(
                url=self.file.url,
                title=self.title,
        )

class Topic(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title
