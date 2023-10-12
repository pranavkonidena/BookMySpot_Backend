from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Backend.models import ModUser,Amenity
from Backend.utils import AuthForHead,createEvent
from Backend.permissions import AmenityHeadPermission
from Backend.serializers import EventSerializer
from rest_framework.exceptions import APIException
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
        return Response("NOPE")
    # amenity_id = amenity.id
    # print(amenity.name)
    # event_name = request.data["event_name"]
    # time_of_occourence_start = request.data["time_start"]
    # time_of_occourence_end = request.data["time_end"]

    # data = createEvent(amenity_id,event_name,time_of_occourence_start,time_of_occourence_end)
    # data = EventSerializer(data)
    else:
        return Response(amenity[0].name)
   
    

    