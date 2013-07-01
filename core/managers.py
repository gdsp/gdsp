import taggit.managers as taggit

# LowerCaseTaggableManager needs to be ignored by South; it inherits from
# django-taggit's TaggableManager which is already ignored by default.
from south.modelsinspector import add_ignored_fields
add_ignored_fields(['^core\.managers\.LowerCaseTaggableManager'])

# The add() method defined in django-taggit's _TaggableManager causes an
# infinite loop when an existing tag is 'added' again with a different
# combination of upper and lower case letters. Because the logic that looks
# for existing tags is in add() case-sensitive, whereas LowerCaseTag's save()
# method is not, the same tag is always considered new causing a World of Hurt.
#
# Monkey patching our Topic's tag manager proved to be infeasible, hence
# the two Manager classes below. The only difference from the original
# django-taggit code is that the tags in add() are all lower-cased, and that
# _TaggableManager is replaced with _LowerCaseTaggableManager in __get__().

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
