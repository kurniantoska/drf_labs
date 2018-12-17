from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drones.models import (DroneCategory, Drone, Pilot, Competition)
from drones.serializers import (DroneCategorySerializer, DroneSerializer, PilotSerializer, PilotCompetitionSerializer)


class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer


class DroneList(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer


class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer


class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer


class ApiRoot(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'drone-categories': reverse('drones:dronecategory-list', request=request),
            'drones': reverse('drones:drone-list', request=request),
            'pilots': reverse('drones:pilot-list', request=request),
            'competition': reverse('drones:competition-list', request=request)
        })
