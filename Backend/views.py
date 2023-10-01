from Backend.models import User,IndividualBooking,Amenity
from Backend.serializers import UserSerializer,IndividualBookingSerializer,TimeSerializer
from rest_framework import generics
from Backend.utils import create_user,GetSlot,doOauth
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
# Create your views here.

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SpecificUser(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        uid = self.request.query_params.get('id')
        if uid is not None:
            queryset = queryset.filter(id=uid)
        return queryset


class IndividualBookingView(generics.ListAPIView):
    serializer_class = IndividualBookingSerializer

    def get_queryset(self):
        queryset = IndividualBooking.objects.all()
        uid = self.request.query_params.get('id')
        if uid is not None:
            queryset = queryset.filter(id=uid)
        return queryset


import datetime
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

@api_view(['POST'])
def getAvailableSlots(request):
    if("location" in request.data):
        data = GetSlot(request.data["duration"] ,  location = request.data["location"])
    elif("amenity" in request.POST):
        data = GetSlot(request.data["duration"] ,  amenity = request.data["amenity"])
    else:
        data = GetSlot(request.data["duration"])
    serialized_data = []
    for item in data:
        for free_slot in item["free_slots"]:
            print(free_slot)
            start_time , end_time = free_slot
            data2 = {
                    'start_time': start_time.strftime('%H:%M'),
                    'end_time': end_time.strftime('%H:%M'),
                    'amenity_id' : item["id"],
                        }
            serializer = TimeSerializer(data=data2)
            if serializer.is_valid():
                serialized_data.append(serializer.validated_data)
            else:
                print(serializer.errors)
    return Response(serialized_data)

@api_view(["GET"])
def userAuth(request):
    data = doOauth(request.query_params.get("code"))
    return Response(data)