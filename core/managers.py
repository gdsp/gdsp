import taggit.managers as taggit

from django.db.models import manager

class TopicManager(manager.Manager):
    """
    The TopicManager class adds some useful methods for fetching topics to
    the default, plain Manager.

    Note: Even though this is the manager for all of Topic, the topics related
          to a Lesson are wrapped in a ManyRelatedManager which filters the
          queryset (returned by all()) to include only the relevant topics.
          I.e., `lesson.topics.first()` will return the first topic for the
          given lesson, not the first of all the topics.
    """

    def first(self):
        """Returns the first topic in the queryset."""
        return self.all()[0]

    def after(self, topic):
        """Takes a topic and returns the succeeding topic in the queryset."""
        topic_ids = [t.id for t in self.all()]
        try:
            current_topic = topic_ids.index(topic.id)
            next_topic = self.get(id=topic_ids[current_topic+1])
            return next_topic
        except (ValueError, IndexError):
            return None

    def before(self, topic):
        """Takes a topic and returns the preceding topic in the queryset."""
        topic_ids = [t.id for t in self.all()]
        try:
            current_topic = topic_ids.index(topic.id)
            if current_topic == 0:
                # A negative index will currently raise an AssertionError,
                # but who knows what the future will bring? Let's just return.
                return None
            previous_topic = self.get(id=topic_ids[current_topic-1])
            return previous_topic
        except (ValueError, IndexError):
            return None

    def contains(self, topic):
        """
        Takes a topic id or a topic instance and returns true if that topic
        is in the queryset, else false.
        """
        if isinstance(topic, self.model):
            topic = topic.id
        return self.filter(id=topic).count() > 0


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
