from movielist.serializers import MovieSerializer, MovieTitleSerializer
from .models import Cinema, Screening, Movie
from rest_framework import serializers


class CinemaSerializer(serializers.HyperlinkedModelSerializer):
    # movies = serializers.SerializerMethodField()
    movies = serializers.HyperlinkedRelatedField(
        view_name='movie-detail',
        read_only=True,
        many=True,
        allow_null=True,

    )

    class Meta:
        model = Cinema
        fields = ["name", "city", "movies"]
