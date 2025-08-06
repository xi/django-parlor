from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import get_language


class TranslationFallback:
    def __getattr__(self, key):
        return 'not translated'


class TranslatableModel(models.Model):
    class Meta:
        abstract = True

    @cached_property
    def translation(self):
        lang = get_language()
        if self.pk:
            try:
                return self.translations.get(language_code=lang)
            except ObjectDoesNotExist:
                pass
        return TranslationFallback()

    def __getattr__(self, key):
        fields = self.translations.model._meta.get_fields()
        if key in (f.attname for f in fields):
            return getattr(self.translation, key)
        else:
            raise AttributeError

    @classmethod
    def lang_field(cls):
        return models.CharField('Language', max_length=15, db_index=True)

    @classmethod
    def parent_field(cls):
        return models.ForeignKey(
            cls,
            on_delete=models.CASCADE,
            editable=False,
            null=True,
            related_name='translations',
        )
