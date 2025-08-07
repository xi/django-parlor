from django.test import TestCase
from django.utils import translation

from .models import MyModel


class TranslatableModelTests(TestCase):
    def test_translation(self):
        animal = MyModel.objects.create()
        animal.translations.create(language_code='en', label='Frog')

        with translation.override('en'):
            self.assertEqual(animal.label, 'Frog')

    def test_override(self):
        animal = MyModel.objects.create()
        animal.translations.create(language_code='en', label='Frog')
        animal.translations.create(language_code='de', label='Frosch')

        with translation.override('en'):
            self.assertEqual(animal.label, 'Frog')
        with translation.override('de'):
            self.assertEqual(animal.label, 'Frosch')

    def test_fallback(self):
        animal = MyModel.objects.create()

        with translation.override('en'):
            self.assertEqual(animal.label, 'not translated')

    def test_non_field(self):
        animal = MyModel.objects.create()

        with self.assertRaises(AttributeError):
            animal.does_not_exist
