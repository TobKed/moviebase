from django.test import TestCase
from showtimes.models import Cinema, Screening
from movielist.models import Movie
from rest_framework.test import APITestCase
from datetime import date

class CinemaBasicTest(TestCase):

    def create_cinema(self, name="only a test", city="only a test"):
        return Cinema.objects.create(name=name, city=city)

    def test_cinema_creation(self):
        c = self.create_cinema()
        self.assertTrue(isinstance(c, Cinema))
        self.assertEqual(c.__str__(), c.name)


class SceeningBasicTest(TestCase):
    def test_create_screening(self):
        with self.assertRaises(Exception):
            Screening.objects.create()


class CinemaMoreTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.c1 = Cinema.objects.create(name="only a test", city="only a test")

    def test_cinema_creation(self):
        c = Cinema.objects.get(id=1)
        self.assertEqual(c.__str__(), c.name)
