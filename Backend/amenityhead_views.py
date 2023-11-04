from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Backend.models import ModUser,Amenity,freeSlots,numbers,IndividualBooking,GroupBooking,Event
from Backend.utils import AuthForHead,createEvent
from Backend.permissions import AmenityHeadPermission
from Backend.serializers import EventSerializer,IndividualBookingSerializer,GroupBookingSerializer , TeamSerializer
from Backend.utils import cancelIndiRes
from rest_framework import generics
import datetime
@api_view(["POST"])
def HeadAuth(request):
    email = request.data["email"]
    password = request.data["password"]
    result = AuthForHead(email,password = password)
    if(result != False):
        m = ModUser.objects.get(email=email)
        return Response(m.id,status=200)
    else:
        return Response("Not an admin head",status=401)


@api_view(["POST"])
@permission_classes([AmenityHeadPermission])
def CreateEventView(request): 
    token = request.data["token"]
    amenity = Amenity.objects.filter(admin=token)
    if(len(amenity) == 0):
        return Response("Amenity not found")
    else:
        amenity_id = amenity[0].id
        print(amenity[0].name)
        event_name = request.data["event_name"]
        time_of_occourence_start = request.data["time_start"]
        time_of_occourence_end = request.data["time_end"]

        data = createEvent(amenity_id,event_name,time_of_occourence_start,time_of_occourence_end)
        data = EventSerializer(data)
        return Response(data.data)
   
    

@api_view(["POST"])
@permission_classes([AmenityHeadPermission])
def setSlotsView(request):
    token = request.data.get("token")
    amenity = Amenity.objects.get(admin=token)
    start_date = request.data.get("start")
    end_date = request.data.get("end")
    start_date_as_list = start_date.split(" ")
    end_date_as_list = end_date.split(" ")
    start_year = int(start_date_as_list[0])
    start_month = int(start_date_as_list[1])
    start_day = int(start_date_as_list[2])

    end_year = int(end_date_as_list[0])
    end_month = int(end_date_as_list[1])
    end_day = int(end_date_as_list[2])

    start_date = datetime.date(start_year,start_month,start_day)
    end_date = datetime.date(end_year,end_month,end_day)
    
    current_date = start_date
    while(current_date <= end_date):
        fe = freeSlots()
        fe.date = current_date
        for i in range(1,57):
            n = numbers.objects.get(value=i)
            fe.save()
            fe.slots.add(n)
            fe.save()  
        fe.amenity = amenity
        fe.save()
        current_date = current_date + datetime.timedelta(days=1)
    
    return Response("Set")


@api_view(["GET"])
def listallBookings(request):
    admin_token = request.query_params.get("id")
    me = ModUser.objects.get(id=admin_token)
    a = Amenity.objects.get(admin=me)
   

    i = IndividualBooking.objects.filter(amenity=a)
    g = GroupBooking.objects.filter(amenity=a)

    total_bookings =  []
    for item in i:
        temp = IndividualBookingSerializer(item)
        temp_data = temp.data
        temp_data["type"] = "Individual"
        total_bookings.append(temp_data)
    
    for item in g:
        temp = GroupBookingSerializer(item)
        temp_data = temp.data
        temp_data["type"] = "Group"
        total_bookings.append(temp_data)
    
    return Response(total_bookings)



