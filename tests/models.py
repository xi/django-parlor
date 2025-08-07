from django.db import models

from parlor.models import TranslatableModel


class MyModel(TranslatableModel):
    pass


class MyModelTranslation(models.Model):
    parent = MyModel.get_parent_field()
    language_code = MyModel.get_language_field()

    label = models.CharField(max_length=32)

    class Meta:
        unique_together = [('parent', 'language_code')]
