from django.test import TestCase
from stgame_recommend.models import UserModel

class AnimalTestCase(TestCase):
    def setUp(self):
        UserModel.objects.create(name="lion", sound="roar")
        UserModel.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = UserModel.objects.get(name="lion")
        cat = UserModel.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')