from .models import Cinema, Screening
from .serializers import CinemaSerializer
from rest_framework import generics
from rest_framework import viewsets


# class CinemaListView(generics.ListCreateAPIView):
#     queryset = Cinema.objects.all()
#     serializer_class = CinemaSerializer

class CinemaViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
