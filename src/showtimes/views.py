from .models import Cinema, Screening
from .serializers import CinemaSerializer
from rest_framework import generics


class CinemaListView(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
