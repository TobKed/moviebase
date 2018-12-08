from django.test import TestCase, mock
from showtimes.models import Cinema, Screening
from movielist.models import Movie, Person
from rest_framework.test import APITestCase
from datetime import date
from random import randint, sample
from faker import Faker


class CinemaBasicTestCase(TestCase):
    def create_cinema(self, name="only a test", city="only a test"):
        return Cinema.objects.create(name=name, city=city)

    def test_cinema_creation(self):
        c = self.create_cinema()
        self.assertTrue(isinstance(c, Cinema))
        self.assertEqual(c.__str__(), c.name)


class CinemaMoreTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.c1 = Cinema.objects.create(name="only a test", city="only a test")

    def test_cinema_creation(self):
        c = Cinema.objects.get(id=1)
        self.assertEqual(c.__str__(), c.name)


class SceeningBasicTestCase(TestCase):
    def test_create_screening(self):
        with self.assertRaises(Exception):
            Screening.objects.create()


class ScreeningTestCase(TestCase):
    def setUp(self):
        """Populate test database with random data."""
        self.faker = Faker("pl_PL")
        for _ in range(5):
            Person.objects.create(name=self.faker.name())
        for _ in range(5):
            self._create_fake_movie()

        for _ in range(5):
            self._create_fake_cinema()

    def _random_person(self):
        """Return a random Person object from db."""
        people = Person.objects.all()
        return people[randint(0, len(people) - 1)]

    def _find_person_by_name(self, name):
        """Return the first `Person` object that matches `name`."""
        return Person.objects.filter(name=name).first()

    def _fake_movie_data(self):
        """Generate a dict of movie data

        The format is compatible with serializers (`Person` relations
        represented by names).
        """
        movie_data = {
            "title": "{} {}".format(self.faker.job(), self.faker.first_name()),
            "description": self.faker.sentence(),
            "year": int(self.faker.year()),
            "director": self._random_person().name,
        }
        people = Person.objects.all()
        actors = sample(list(people), randint(1, len(people)))
        actor_names = [a.name for a in actors]
        movie_data["actors"] = actor_names
        print(movie_data["title"])
        return movie_data

    def _create_fake_movie(self):
        """Generate new fake movie and save to database."""
        movie_data = self._fake_movie_data()
        movie_data["director"] = self._find_person_by_name(movie_data["director"])
        actors = movie_data["actors"]
        del movie_data["actors"]
        new_movie = Movie.objects.create(**movie_data)
        for actor in actors:
            new_movie.actors.add(self._find_person_by_name(actor))

    def _create_fake_cinema(self):
        """Generate new fake cinema and save to database."""
        name = self.faker.company()
        city = self.faker.city()
        movies = Movie.objects.all()
        movies = sample(list(movies), randint(1, len(movies)))
        cinema = Cinema.objects.create(name=name, city=city)
        cinema.movies_set = movies

    def test_create_screening(self):
        with self.assertRaises(Exception):
            Screening.objects.create()
