from Backend.models import User,IndividualBooking,Amenity
from Backend.serializers import UserSerializer,IndividualBookingSerializer,TimeSerializer
from rest_framework import generics
from Backend.utils import GetSlot,doOauth,makeIndiRes,cancelIndiRes
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
            queryset = queryset.filter(booker_id=uid)
        return queryset


import datetime
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

@api_view(['POST'])
def getAvailableSlots(request):
    if("location" in request.data and "amenity" in request.data):
        data = GetSlot(request.data["duration"] ,  location = request.data["location"] , amenity=request.data["amenity"])
    elif("amenity" in request.data):
        data = GetSlot(request.data["duration"] ,  amenity = request.data["amenity"])
    elif("location" in request.data):
        data = GetSlot(request.data["duration"],location=request.data["location"])
    else:
        data = GetSlot(request.data["duration"])
    serialized_data = []
    print(len(serialized_data))
    if("start_time" in request.data):
        for item in data:
            for free_slot in item["free_slots"]:
                start_time , end_time = free_slot
                string_as_list = request.data["start_time"].split(":")
                hours = int(string_as_list[0])
                minutes = string_as_list[1]
                if(abs(hours-int(start_time.hour)) < 1):
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
    else:
        for item in data:
            for free_slot in item["free_slots"]:
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

@api_view(["POST"])
def makeIndiReservation(request):
    amenity_id = request.data["amenity_id"]
    start_time = request.data["start_time"]
    end_time = request.data["end_time"]
    id_user = request.data["id_user"]
    data = makeIndiRes(id_user,amenity_id,start_time,end_time)

    data = IndividualBookingSerializer(data)
    return Response(data.data)

@api_view(["GET"])
def cancelIndiReservation(request):
    booking_id= request.query_params.get("booking_id")
    cancelIndiRes(booking_id)
    return Response("OK")
