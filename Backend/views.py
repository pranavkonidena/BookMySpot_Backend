from Backend.models import User,IndividualBooking,Amenity
from Backend.serializers import UserSerializer,IndividualBookingSerializer,AmenitySerializer
from rest_framework import generics
from Backend.utils import create_user
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



@api_view(['POST'])
def getAvailableSlots(request):
    queryset = Amenity.objects.all()
    name = request.data["name"]
    if name is not None:
        queryset = queryset.filter(name=name)
    
    data = AmenitySerializer(queryset , many = True)
    return Response(data=data.data)

