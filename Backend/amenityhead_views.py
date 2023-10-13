from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Backend.models import ModUser,Amenity,freeSlots,numbers
from Backend.utils import AuthForHead,createEvent
from Backend.permissions import AmenityHeadPermission
from Backend.serializers import EventSerializer
import datetime
@api_view(["POST"])
def HeadAuth(request):
    email = request.data["email"]
    password = request.data["password"]
    result = AuthForHead(email,password = password)
    if(result != False):
        return Response(result,status=200)
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
        amenity_id = amenity.id
        print(amenity.name)
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