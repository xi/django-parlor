from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import get_language


class TranslationFallback:
    def __getattr__(self, key):
        return 'not translated'


class TranslatableModel(models.Model):
    class Meta:
        abstract = True

    @property
    def translation(self):
        if not self.pk:
            return TranslationFallback()

        lang = get_language()

        translation = self.__dict__.get('_translation')
        if translation and translation.language_code == lang:
            return translation

        try:
            translation = self.translations.get(language_code=lang)
            self.__dict__['_translation'] = translation
            return translation
        except ObjectDoesNotExist:
            return TranslationFallback()

    def refresh_from_db(self, *args, **kwargs):
        self.__dict__.pop('_translation', None)
        return super().refresh_from_db(*args, **kwargs)

    def __getattr__(self, key):
        fields = self.translations.model._meta.get_fields()
        if key in (f.attname for f in fields):
            return getattr(self.translation, key)
        else:
            raise AttributeError

    @classmethod
    def get_language_field(cls):
        return models.CharField('Language', max_length=15, db_index=True)

    @classmethod
    def get_parent_field(cls):
        return models.ForeignKey(
            cls,
            on_delete=models.CASCADE,
            editable=False,
            null=True,
            related_name='translations',
        )
