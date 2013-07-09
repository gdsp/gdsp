import taggit.managers as taggit

from django.db.models import manager, Count

class LessonManager(manager.Manager):

    def have_topics(self):
        """Returns all lessons that have topics associated with them."""
        return self.annotate(
                topics_count=Count('topics'),
        ).filter(topics_count__gt=0)

class LessonTopicManager(manager.Manager):
    """
    LessonTopicManager adds some useful methods for fetching lesson-topic
    relations relative to a lesson or another lesson-topic relation.

    It is often necessary to go through a lesson-topic relation when what you
    really want is a topic because the order of a lesson's topics is stored in
    the relation objects, not in the lesson or topics.
    """

    def first(self, lesson):
        """
        Takes a lesson object or a lesson id and returns the first lesson-topic
        relation for that lesson.
        """
        if not isinstance(lesson, int):
            lesson = lesson.id
        try:
            return self.filter(lesson=lesson)[0]
        except IndexError:
            return None

    def after(self, lesson_topic):
        """
        Takes a lesson-topic relation and returns the next one in the lesson.
        """
        ids = [rel.id for rel in self.filter(lesson=lesson_topic.lesson.id)]
        try:
            current_rel = self.get(
                    lesson=lesson_topic.lesson.id,
                    topic=lesson_topic.topic.id,
            )
            current_index = ids.index(current_rel.id)
            next_rel = self.get(id=ids[current_index+1])
            return next_rel
        except (ValueError, IndexError):
            return None

    def before(self, lesson_topic):
        """
        Takes a lesson-topic relation and returns the previous one
        in the lesson.
        """
        ids = [rel.id for rel in self.filter(lesson=lesson_topic.lesson.id)]
        try:
            current_rel = self.get(
                    lesson=lesson_topic.lesson.id,
                    topic=lesson_topic.topic.id,
            )
            current_index = ids.index(current_rel.id)
            if current_index == 0:
                # A negative index will currently raise an AssertionError,
                # but who knows what the future will bring? Let's just return.
                return None
            previous_rel = self.get(id=ids[current_index-1])
            return previous_rel
        except (ValueError, IndexError):
            return None


# LowerCaseTaggableManager needs to be ignored by South; it inherits from
# django-taggit's TaggableManager which is already ignored by default.
from south.modelsinspector import add_ignored_fields
add_ignored_fields(['^core\.managers\.LowerCaseTaggableManager'])

################################################################################
# The add() method defined in django-taggit's _TaggableManager causes an       #
# infinite loop when an existing tag is 'added' again with a different         #
# combination of upper and lower case letters. Because the logic that looks    #
# for existing tags is in add() case-sensitive, whereas LowerCaseTag's save()  #
# method is not, the same tag is always considered new causing a World of      #
# Hurt.                                                                        #
#                                                                              #
# Monkey patching our Topic's tag manager proved to be infeasible, hence       #
# the two Manager classes below. The only difference from the original         #
# django-taggit code is that the tags in add() are all lower-cased, and that   #
# _TaggableManager is replaced with _LowerCaseTaggableManager in __get__().    #
################################################################################

class _LowerCaseTaggableManager(taggit._TaggableManager):
    def add(self, *tags):
        tags = [tag.lower() for tag in tags]
        super(_LowerCaseTaggableManager, self).add(*tags)


class LowerCaseTaggableManager(taggit.TaggableManager):
    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError(
                    '{} objects need to have a primary key value before ' \
                    'you can access their tags.'.format(model.__name__)
            )
        manager = _LowerCaseTaggableManager(through=self.through, model=model,
                                            instance=instance)
        return manager
