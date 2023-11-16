from Backend.models import User,IndividualBooking,Event,GroupBooking,Amenity,Group,ModUser,freeSlots
from Backend.serializers import UserSerializer,IndividualBookingSerializer,TimeSerializer,EventSerializer,AmenitySerializer
from rest_framework import generics
from Backend.utils import GetSlot,doOauth,makeIndiRes,cancelIndiRes
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
import os
import requests
from dotenv import load_dotenv
load_dotenv()
from rest_framework import status
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
    date = request.data["date"]
    format = '%Y-%m-%d'
    datetime_str = datetime.datetime.strptime(date , format)

    if("location" in request.data and "amenity" in request.data):
        data = GetSlot(request.data["duration"] ,datetime_str, location = request.data["location"] , amenity=request.data["amenity"])
    elif("amenity" in request.data):
        data = GetSlot(request.data["duration"] ,datetime_str , amenity = request.data["amenity"])
    elif("location" in request.data):
        data = GetSlot(request.data["duration"],datetime_str,location=request.data["location"])
    else:
        data = GetSlot(request.data["duration"],datetime_str)
    serialized_data = []
    print(len(serialized_data))
    if(data is None):
        return Response("[]")
    else:
        if("start_time" in request.data):
            for item in data:
                for free_slot in item["free_slots"]:
                    start_time , end_time = free_slot
                    string_as_list = request.data["start_time"].split(":")
                    hours = int(string_as_list[0])
                    minutes = string_as_list[1]
                    if(abs(hours-int(start_time.hour)) < 1):
                        data2 = {
                                'start_time': str(start_time.strftime('%H:%M')),
                                'end_time': str(end_time.strftime('%H:%M')),
                                'amenity_id' : item["id"],
                                    }
                        serialized_data.append(data2)
            return Response(serialized_data)
        else:
            for item in data:
                for free_slot in item["free_slots"]:
                    start_time , end_time = free_slot
                    data2 = {
                            'start_time': str(start_time.strftime('%H:%M')),
                            'end_time': str(end_time.strftime('%H:%M')),
                            'amenity_id' : item["id"],
                                }
                    serialized_data.append(data2)
            return Response(serialized_data)

from django.http import HttpResponseRedirect
data_filled = None
@api_view(["GET"])
def userAuth(request):
    code = request.query_params.get("code")
    try:
        print(code)
        data_filled = doOauth(code)
        return Response(data_filled , status=status.HTTP_200_OK)
    except:
        return Response("Error Logging You In" , status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def getuserAuth(request):
    global data_filled
    if(data_filled != None):
        return Response(data_filled)
    else:
        return Response(status=500)


@api_view(["GET"])
def redirectuserAuth(request):
   oauth_uri = os.environ.get("OAUTH_URI")
   return HttpResponseRedirect(oauth_uri)

@api_view(["POST"])
def makeIndiReservation(request):
    amenity_id = request.data["amenity_id"]
    start_time = request.data["start_time"]
    end_time = request.data["end_time"]
    id_user = request.data["id_user"]
    date = request.data["date"]
    amenity = Amenity.objects.get(id=amenity_id)
    format = '%Y-%m-%d'
    date_time_str = datetime.datetime.strptime(date , format)
    data = makeIndiRes(id_user,amenity_id,start_time,end_time,date_time_str)
    if(data == -1):
        return Response("Insufficient Credits" , status=status.HTTP_412_PRECONDITION_FAILED)
    # data = IndividualBookingSerializer(data)
    bookings = []
    entry = {}
    entry["id"] = data["id"]
    entry["type"] = "individual"
    entry["time_of_slot"] = str(data["time_of_slot"])
    entry["duration_of_booking"] = data["duration_of_booking"]
    entry["timestamp_of_booking"] = str(data["timestamp_of_booking"])
    entry["amenity"] = {"name" : amenity.name, "venue" : amenity.venue}
    json_entry = json.dumps(entry)
    bookings.append(json_entry)
    return Response(bookings , status=status.HTTP_200_OK)

@api_view(["DELETE"])
def cancelIndiReservation(request):
    try:
        booking_id= request.data.get("booking_id")
        cancelIndiRes(booking_id)
        return Response("Ok" , status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response("Failed" , status.HTTP_500_INTERNAL_SERVER_ERROR)

class EventsList(generics.ListAPIView):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.all()
        queryset = queryset.filter(time_of_occourence_start__gt = datetime.datetime.now())
        token = self.request.query_params.get("id")
        id = self.request.query_params.get("event_id")
        if id is not None:
            queryset = queryset.filter(id=id)
        if(token != None):
            me = ModUser.objects.get(id=token)
            a = Amenity.objects.get(admin=me)
            queryset = queryset.filter(amenity=a)
        
        return queryset

import json
@api_view(["GET" , "POST"])
def getBooking(request):
    if(request.method == "POST"):
        user_id = request.data["id"]
        date = request.data["date"]
        date = datetime.datetime.strptime(date , '%Y-%m-%d')
        indi = IndividualBooking.objects.filter(booker_id=user_id)
        groups = Group.objects.filter(member=user_id)
        bookings = []
        time = datetime.datetime.now()
        for item in indi:
            if(item.time_of_slot.day == date.day and item.time_of_slot.month == date.month and item.time_of_slot.year == date.year):
                amenity = Amenity.objects.get(id=item.amenity.id)
                entry = {}
                entry["id"] = item.id
                entry["type"] = "individual"
                entry["time_of_slot"] = str(item.time_of_slot)
                entry["duration_of_booking"] = item.duration_of_booking
                entry["timestamp_of_booking"] = str(item.timestamp_of_booking)
                entry["amenity"] = {"name" : amenity.name, "venue" : amenity.venue}
                json_entry = json.dumps(entry)
                bookings.append(json_entry)
        
        
        for item in groups:
            bookings_groups = GroupBooking.objects.filter(booker=item.id)
            group_entry = {}
            group_entry["name"] = item.name
            group_entry["members"] = [member.id for member in item.member.all()]  # Convert ManyToMany to a list of IDs
            group_entries = []
            
            for booking in bookings_groups:
                print(booking.time_of_slot)
                if(booking.time_of_slot.day ==  date.day and booking.time_of_slot.month == date.month and booking.time_of_slot.year == date.year):
                # if(time_diff > 0):
                    amenity = Amenity.objects.get(id=booking.amenity.id)
                    entry = {}
                    entry["id"] = booking.id
                    entry["type"] = "group"
                    entry["time_of_slot"] = str(booking.time_of_slot)
                    entry["duration_of_booking"] = booking.duration_of_booking
                    entry["timestamp_of_booking"] = str(booking.timestamp_of_booking)
                    entry["amenity"] = {"name": amenity.name, "venue": amenity.venue}
                    entry["group"] = group_entry
                    group_entries.append(entry)
            
            bookings.extend(group_entries)

        return Response(bookings , status=status.HTTP_200_OK)
    elif(request.method == "GET"):
        booking_id = request.query_params.get("id")
        try:
            item = IndividualBooking.objects.get(id=booking_id)
            amenity = Amenity.objects.get(id=item.amenity.id)
            entry = {}
            entry["id"] = item.id
            entry["type"] = "individual"
            entry["time_of_slot"] = str(item.time_of_slot)
            entry["duration_of_booking"] = item.duration_of_booking
            entry["timestamp_of_booking"] = str(item.timestamp_of_booking)
            entry["amenity"] = {"name" : amenity.name, "venue" : amenity.venue}
            json_entry = json.dumps(entry)
            return Response(json_entry , status=status.HTTP_200_OK)
        except:
            item = GroupBooking.objects.get(id=booking_id)
            group = item.booker
            group_entry = {}
            group_entry["name"] = item.name
            group_entry["members"] = [member.id for member in item.member.all()]
            amenity = Amenity.objects.get(id=booking.amenity.id)
            entry = {}
            entry["id"] = booking.id
            entry["type"] = "group"
            entry["time_of_slot"] = str(booking.time_of_slot)
            entry["duration_of_booking"] = booking.duration_of_booking
            entry["timestamp_of_booking"] = str(booking.timestamp_of_booking)
            entry["amenity"] = {"name": amenity.name, "venue": amenity.venue}
            entry["group"] = group_entry
            group_entries.append(entry)
            return Response(entry , status=status.HTTP_200_OK)
        

    

class AmenitiesList(generics.ListAPIView):
    serializer_class = AmenitySerializer
    
    def get_queryset(self):
        queryset = Amenity.objects.all()
        id = self.request.query_params.get("id")
        if(id is not None):
            queryset = queryset.filter(id=id)
        
        return queryset

class BookingDetails(generics.ListAPIView):
    serializer_class = IndividualBookingSerializer

    def get_queryset(self):
        queryset = IndividualBooking.objects.all()
        id = self.request.query_params.get("id")
        if id is not None:
            queryset = queryset.filter(id=id)
        
        return queryset

@api_view(["POST"])
def getAvailableAmenities(request):
    date = request.data["date"]
    date = datetime.datetime.strptime(date , "%Y-%m-%d")

    a = Amenity.objects.all()
    final_list = []
    for item in a:
        try:
            f = freeSlots.objects.filter(amenity=item)
            if f is not None:
                f = f.get(date=date)
                if(len(f.slots.all()) != 0):
                    final_list.append(AmenitySerializer(item).data)
        except:
            pass
    return Response(final_list)

