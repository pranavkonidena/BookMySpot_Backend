from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Backend.models import ModUser
from Backend.models import ValidEmails
from Backend.utils import AuthForHead
from Backend.permissions import AmenityHeadPermisson
@api_view(["POST"])
def HeadAuth(request):
    email = request.data["email"]
    password = request.data["password"]
    result = AuthForHead(email,password = password)
    if(result == True):
        return Response("OK",status=200)
    else:
        return Response("Not an admin head",status=401)

@api_view(["POST" , "GET"])
@permission_classes([AmenityHeadPermisson])
def DontKnow(request):    
    return Response("Amenity heads only")
    