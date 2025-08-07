from django.db import models
from django.utils.translation import get_language


class TranslatableModel(models.Model):
    class Meta:
        abstract = True

    @property
    def translation(self):
        translation = self.__dict__.get('_translation')
        if translation and translation.language_code == get_language():
            return translation

        if not self.pk:
            raise self.translations.model.DoesNotExist

        translation = self.translations.get(language_code=get_language())
        self.__dict__['_translation'] = translation
        return translation

    def refresh_from_db(self, *args, **kwargs):
        self.__dict__.pop('_translation', None)
        return super().refresh_from_db(*args, **kwargs)

    def __getattr__(self, key):
        fields = self.translations.model._meta.get_fields()
        if key not in (f.attname for f in fields):
            raise AttributeError
        try:
            return getattr(self.translation, key)
        except self.translations.model.DoesNotExist:
            return 'not translated'

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
