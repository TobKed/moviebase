from django.test import TestCase, mock
from showtimes.models import Cinema, Screening
from movielist.models import Movie, Person
from rest_framework.test import APITestCase
from datetime import date
from random import randint, sample, choice
from faker import Faker


class FakeData:
    def __init__(self):
        """Populate test database with random data."""
        self.faker = Faker("pl_PL")
        for _ in range(5):
            Person.objects.create(name=self.faker.name())
        for _ in range(5):
            self._create_fake_movie()
        for _ in range(5):
            self._create_fake_cinema()
        for _ in range(5):
            self._create_fake_screening()

    def _random_person(self):
        """Return a random Person object from db."""
        people = Person.objects.all()
        return people[randint(0, len(people) - 1)]
    
    def _random_movie(self):
        """Return a random Movie object from db."""
        movie = Movie.objects.all()
        return movie[randint(0, len(movie) - 1)]
    
    def _random_cinema(self):
        """Return a random Cinema object from db."""
        cinema = Cinema.objects.all()
        return cinema[randint(0, len(cinema) - 1)]
    
    def _random_screening(self):
        """Return a random Cinema object from db."""
        screening = Screening.objects.all()
        return screening[randint(0, len(screening) - 1)]

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

    def _create_fake_screening(self):
        """Generate new fake screening and save to database."""
        cinema = choice(Cinema.objects.all())
        movie = choice(Movie.objects.all())
        dete_ = self.faker.date()
        Screening.objects.create(cinema=cinema, movie=movie, date=dete_)


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
    @classmethod
    def setUpTestData(cls):
        cls.fake_data = FakeData()

    def test_create_screening(self):
        with self.assertRaises(Exception):
            Screening.objects.create()

    def test_get_cinemas_list(self):
        response = self.client.get(path="/cinemas/", data={}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cinema.objects.count(), len(response.data))
