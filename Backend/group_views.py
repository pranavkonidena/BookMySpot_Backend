from Backend.models import Group
from Backend.serializers import GroupSerializer,GroupBookingSerializer
from rest_framework import generics
from Backend.utils import  addtoGrp,groupReservation
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

class GroupList(generics.ListAPIView):
    serializer_class = GroupSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        
        queryset = Group.objects.all()
        uid = self.request.query_params.get('id')
        if uid is not None:
            queryset = queryset.filter(member=uid)
        return queryset
        

@api_view(['POST'])
def memberAdd(request):
    addtoGrp(request.data["name"] , request.data["id"])
    return Response(request.data["id"])

@api_view(['POST'])
def groupReservationView(request):
    amenity_id = request.data["amenity_id"]
    start_time = request.data["start_time"]
    end_time = request.data["end_time"]
    group_id = request.data["group_id"]
    data = groupReservation(group_id,start_time,end_time,amenity_id)

    data = GroupBookingSerializer(data)
    return Response(data.data)