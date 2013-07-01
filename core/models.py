import markdown
import model_utils.managers
import pygments
import pygments.formatters
import pygments.lexers
import taggit.models

from django.db import models
from django.core.urlresolvers import reverse

from managers import LowerCaseTaggableManager


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
    # The element_type is set in the save() method of the subclass, and will
    # be the same for all elements of a given type. This reduces the number of
    # database queries needed to determine a BaseTopicElement's actual type
    # when compared to iterating over the possible subclasses and looking for
    # an attribute of that name. It is, of course, data duplication, but the
    # speed-up is worth it.
    element_type = models.CharField(max_length=16, blank=False, editable=False)

    # model_utils.managers.InheritanceManager allows us to fetch subclass
    # objects as instances of those subclasses rather than as instances of
    # BaseTopicElement. This means that the correct to_html() method will be
    # called in our views.
    objects = model_utils.managers.InheritanceManager()

    def to_html(self):
        raise NotImplementedError

    def __unicode__(self):
        return self.description

    class Meta:
        order_with_respect_to = 'topic'


class MarkdownElement(BaseTopicElement):
    """
    A topic element containing text written in the Markdown
    markup language.
    """

    text = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = 'text'
        super(MarkdownElement, self).save(*args, **kwargs)

    def to_html(self):
        return markdown.markdown(self.text)

    class Meta:
        verbose_name = 'text element'


class CodeElement(BaseTopicElement):
    """
    A topic element containing example code. Its HTML representation is
    produced by Pygments attempting to guess the programming language and
    add markup for syntax highlighting.
    """

    code = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = 'code'
        super(CodeElement, self).save(*args, **kwargs)

    def to_html(self):
        return pygments.highlight(
                self.code,
                pygments.lexers.guess_lexer(self.code),
                pygments.formatters.HtmlFormatter(),
        )


class ImageElement(BaseTopicElement):
    """
    A topic element containing an image and, optionally, a caption.
    Its  HTML representation wraps the image and caption (if present)
    in a figure element.
    """

    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='images')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = 'image'
        super(ImageElement, self).save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = 'audio'
        super(AudioElement, self).save(*args, **kwargs)

    def to_html(self):
        return u'<a class="audio-element" href="{url}">{title}</a>'.format(
                url=self.file.url,
                title=self.title,
        )


class LowerCaseTag(taggit.models.TagBase):
    """
    A django-taggit tag which forces the tag name to be lower-case in order to
    avoid having two separate tags named, say, 'time-based' and 'Time-based'.
    """

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(LowerCaseTag, self).save(*args, **kwargs)


class LowerCaseTaggedItem(taggit.models.GenericTaggedItemBase):
    """
    An intermediary model which enables case-insensitive (forced lower-case)
    tags with django-taggit.

    See: http://django-taggit.readthedocs.org/en/latest/custom_tagging.html
    """

    tag = models.ForeignKey(LowerCaseTag, related_name='tagged_items')


class Topic(models.Model):
    """
    A topic is an ordered collection of topic elements relished with a title
    and a collection of tags. It constitutes one web page of content and part
    of a lesson.
    """

    title = models.CharField(max_length=255)
    tags = LowerCaseTaggableManager(
            through=LowerCaseTaggedItem,
            help_text='A comma-separated list of keywords that describe ' \
                      'this topic.',
            blank=True,
    )

    def get_absolute_url(self):
        return reverse('core:topic', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.title


class Lesson(models.Model):
    """
    A lesson is an ordered collection of topics.
    """

    title = models.CharField(max_length=255)
    topics = models.ManyToManyField(Topic, through='LessonTopicRelation')

    def __unicode__(self):
        return self.title


class LessonTopicRelation(models.Model):
    topic = models.ForeignKey(Topic)
    lesson = models.ForeignKey(Lesson)
    topic_ordinal = models.PositiveIntegerField()

    class Meta:
        ordering = ['lesson', 'topic_ordinal']
        index_together = [
                ['lesson', 'topic_ordinal'],
        ]
