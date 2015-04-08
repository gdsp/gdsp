import markdown
import model_utils.managers
import pygments
import pygments.formatters
import pygments.lexers
import taggit.models

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from managers import LessonManager, LessonTopicManager, LowerCaseTaggableManager

from tutor.tests import find_tagged_tests
from tutor.tests import find_inc_files
from multiple import MultiSelectField

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^core\.multiple\.MultiSelectField"])

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

    AUDIO, CODE, IMAGE, MATH, TEXT, TEST, RESULTS = 'audio', 'code', 'image', 'math', 'text', 'test', 'results'
    ELEMENT_TYPES = (
            (AUDIO, _('Audio')),
            (CODE, _('Code')),
            (IMAGE, _('Imagery')),
            (MATH, _('Mathematics')),
            (TEXT, _('Text')),
            (TEST, _('Test')),
            (RESULTS, _('Results')),
    )

    description = models.CharField(
            max_length=255,
            help_text=_('What does this element contain?'),
    )
    topic = models.ForeignKey('Topic', related_name='elements')
    # The element_type is set in the save() method of the subclass, and will
    # be the same for all elements of a given type; its value should be one
    # of the ELEMENT_TYPES defined above, e.g. AUDIO ('audio'). This reduces
    # the number of database queries needed to determine a BaseTopicElement's
    # actual type when compared to iterating over the possible subclasses
    # and looking for an attribute of that name. It is, of course, data
    # duplication, but the speed-up is worth it.
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

    text = models.TextField(
            help_text=_('Markdown-formatted text. '
                        'For information about Markdown, please see the '
                        '<a href="http://daringfireball.net/projects/markdown">'
                        'official documentation</a>.'),
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = BaseTopicElement.TEXT
        super(MarkdownElement, self).save(*args, **kwargs)

    def to_html(self):
        return markdown.markdown(self.text)

    class Meta:
        verbose_name = _('text element')
        verbose_name_plural = _('text elements')


class CodeElement(BaseTopicElement):
    """
    A topic element containing example code. Its HTML representation is
    produced by Pygments attempting to guess the programming language and
    add markup for syntax highlighting.
    """

    code = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = BaseTopicElement.CODE
        super(CodeElement, self).save(*args, **kwargs)

    def to_html(self):
        return pygments.highlight(
                self.code,
                pygments.lexers.guess_lexer(self.code),
                pygments.formatters.HtmlFormatter(),
        )

    class Meta:
        verbose_name = _('code element')
        verbose_name_plural = _('code elements')


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
            self.element_type = BaseTopicElement.IMAGE
        super(ImageElement, self).save(*args, **kwargs)

    def to_html(self):
        if self.description == 'Lesson top':
            html = u'<img class="lesson-intro-img" src="{}">'.format(self.image.url)            
        else:
            html = u'<figure class="image-element">'
            html += u'<img style="max-width: 100%" src="{}">'.format(self.image.url)
        if self.caption:
            html += u'<figcaption>{}</figcaption>'.format(self.caption)
        html += u'</figure>' 
        return html

    class Meta:
        verbose_name = _('image element')
        verbose_name_plural = _('image elements')


class AudioElement(BaseTopicElement):
    """
    A topic element containing an audio file and a title. Its HTML
    representation is a link which, if all goes well, plays / stops
    the audio when clicked; if a problem occurs, it falls back to
    being a regular link allowing the student to download the file.
    """

    title = models.CharField(
            max_length=128,
            help_text=_('The title of the track as displayed to the student.'),
    )
    file = models.FileField(upload_to='audio')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = BaseTopicElement.AUDIO
        super(AudioElement, self).save(*args, **kwargs)

    def to_html(self):
        return u'<a class="audio-element" href="{url}">{title}</a>'.format(
                url=self.file.url,
                title=self.title,
        )

    class Meta:
        verbose_name = _('audio element')
        verbose_name_plural = _('audio elements')


# This method is called from the initialization variable - and
# therefore cannot be part of the class. It is therefore left outside.
def test_choices():
    indices = []
    choices = []
    for tag in find_tagged_tests():
        indices.append('')
        choices.append('tag: ' + tag[0])
        for choice in tag[1]:
            indices.append(choice)
            choices.append(' - ' + choice)
        indices.append('')
        choices.append('')
    return zip(indices, choices)

class TestElement(BaseTopicElement):
    """"
    Integration with the automatic tutor. The test is embedded via an iframe,
    which makes it very easy to just use the tutor app standalone.
    """
    
    test = models.CharField(max_length=256,choices=test_choices())
    difficulty = models.CharField(max_length=256,choices=(('Easy', 'Easy'), ('Hard', 'Hard')))
    effect_files = MultiSelectField(default='NULL.inc', max_length=10000,
                                    choices=tuple([ (fx,fx) for fx in find_inc_files() + ['ALL FX', 'Effects the student has seen so far' ]]))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = BaseTopicElement.TEST
        super(TestElement, self).save(*args, **kwargs)

    def to_html(self):
        current_site = Site.objects.get_current()
        return u'<h2>{description}</h2><iframe src="http://{domain}/tutor/{test}/{difficulty}/{FX}" frameborder="0" scrolling="no" width="100%" height=300"></iframe>'.format(domain=current_site.domain,
                                                                                                                                                  description=self.description, test=self.test, difficulty = self.difficulty, FX=str(' '.join(self.effect_files)))

    class Meta:
        verbose_name = _('test element')
        verbose_name_plural = _('test elements')

class ResultsElement(BaseTopicElement):
    """"
    Displays the aggregated results for the student.
    """

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = BaseTopicElement.RESULTS
        super(ResultsElement, self).save(*args, **kwargs)

    def to_html(self):
        current_site = Site.objects.get_current()
        return u'<h2>{description}</h2><iframe src="http://{domain}/tutor/results" frameborder="0" scrolling="no" width="100%" height=500;"></iframe>'.format(domain=current_site.domain, description=self.description)

    class Meta:
        verbose_name = _('results element')
        verbose_name_plural = _('results elements')

class MathElement(BaseTopicElement):
    """
    A topic element containing equations, formulae or other mathematical
    writing expressed in the LaTeX markup language and rendered to HTML+CSS
    client-side by the MathJax JavaScript library.
    """

    latex = models.TextField(
            help_text=_('LaTeX-formatted mathematics. Remember to enclose '
                        'your markup in delimiters, like so: '
                        '<code>\[ 2^3 = 8 \]</code>.'),
    )
    caption = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.element_type = BaseTopicElement.MATH
        super(MathElement, self).save(*args, **kwargs)

    def to_html(self):
        html = u'<figure class="math-element">'
        html += u'<p>{}</p>'.format(self.latex)
        if self.caption:
            html += u'<figcaption>{}</figcaption>'.format(self.caption)
        html += u'</figure>'
        return html

    class Meta:
        verbose_name = _('math element')
        verbose_name_plural = _('math elements')


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
    caption = models.CharField(max_length=255, null=True,
                                  default='',
                                  help_text=_('The title that will be displayed '
                        '(use if different from title)'),)
    tags = LowerCaseTaggableManager(
            through=LowerCaseTaggedItem,
            help_text=_('A comma-separated list of keywords that describe '
                        'this topic.'),
            blank=True,
    )

    def get_absolute_url(self):
        return reverse('core:topic', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.title

    def display_title(self):
        return self.caption if self.caption else self.title

    class Meta:
        # NOTE: Because lesson-topic relations which are unique may
        #       well include topics which are not, this ordering causes
        #       Topic.objects.all() to return the same topic once for
        #       every relation it is part of. If you need actually
        #       distinct topics, specify a different ordering, e.g.
        #       Topic.objects.order_by('id').
        ordering = [
                'lessontopicrelation__lesson',
                'lessontopicrelation__topic_ordinal',
        ]
        verbose_name = _('topic')
        verbose_name_plural = _('topics')


class Lesson(models.Model):
    """
    A lesson is an ordered collection of topics.
    """

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images', default = 'no-img.jpg')
    course = models.ForeignKey('Course', related_name='lessons')
    topics = models.ManyToManyField(Topic, through='LessonTopicRelation')
    objects = LessonManager()

    def get_absolute_url(self):
        return reverse('core:lesson', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('lesson')
        verbose_name_plural = _('lessons')
        order_with_respect_to = 'course'


class LessonTopicRelation(models.Model):
    topic = models.ForeignKey(Topic)
    lesson = models.ForeignKey(Lesson)
    topic_ordinal = models.PositiveIntegerField()
    # excluded_content is a comma-separated list of topic element types
    # which should not be displayed in this lesson, e.g. 'code, audio':
    excluded_content = models.CharField(max_length=255, blank=True)
    objects = LessonTopicManager()

    @property
    def excludes(self):
        return (e.strip() for e in self.excluded_content.split(','))

    @property
    def topic_elements(self):
        return self.topic.elements.select_subclasses().exclude(
                element_type__in=self.excludes,
        )

    @property
    def next(self):
        return LessonTopicRelation.objects.after(self)

    @property
    def previous(self):
        return LessonTopicRelation.objects.before(self)

    def __unicode__(self):
        return u'Topic: "{}", Lesson: "{}"'.format(self.topic, self.lesson)

    class Meta:
        ordering = ['lesson', 'topic_ordinal']
        index_together = [
                ['lesson', 'topic_ordinal'],
        ]
        verbose_name = _('lesson topic')
        verbose_name_plural = _('lesson topics')


class Course(models.Model):
    """
    A course is an ordered collection of lessons.
    """

    title = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('core:course', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
