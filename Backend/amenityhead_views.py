from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Backend.models import ModUser
from Backend.utils import AuthForHead,createEvent
from Backend.permissions import AmenityHeadPermisson
from Backend.serializers import EventSerializer
@api_view(["POST"])
def HeadAuth(request):
    email = request.data["email"]
    password = request.data["password"]
    result = AuthForHead(email,password = password)
    if(result == True):
        return Response("OK",status=200)
    else:
        return Response("Not an admin head",status=401)

@api_view(["POST"])
@permission_classes([AmenityHeadPermisson])
def CreateEventView(request): 
    if(request.method == "POST"):   
        amenity_id = request.data["amenity_id"]
        event_name = request.data["event_name"]
        time_of_occourence_start = request.data["time_start"]
        time_of_occourence_end = request.data["time_end"]

        data = createEvent(amenity_id,event_name,time_of_occourence_start,time_of_occourence_end)
        data = EventSerializer(data)
        return Response(data.data)
    else:
        return Response("OK")