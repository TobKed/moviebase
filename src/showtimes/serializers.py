from movielist.serializers import MovieSerializer, MovieTitleSerializer
from .models import Cinema, Screening, Movie
from rest_framework import serializers


class CinemaSerializer(serializers.HyperlinkedModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Cinema
        fields = ["name", "city", "movies"]

    def get_movies(self, obj):
        # return {s.movie.__str__() for s in Screening.objects.filter(cinema=obj)}
        # return {MovieSerializer(s.movie, many=False).data.get("title") for s in Screening.objects.filter(cinema=obj)}
        # m_set = list({s.movie for s in Screening.objects.filter(cinema=obj)})
        m_set = {s.movie for s in obj.screening_set.all()}
        return MovieTitleSerializer(m_set, many=True).data
