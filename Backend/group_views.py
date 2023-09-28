from Backend.models import Group
from Backend.serializers import GroupSerializer
from rest_framework import generics
from Backend.utils import  addtoGrp
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from Backend.permissions import TeamAdminPermission

class GroupList(generics.ListAPIView):
    serializer_class = GroupSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        try:
            queryset = Group.objects.all()
            uid = self.request.query_params.get('id')
            if uid is not None:
                queryset = queryset.filter(member=uid)
            return queryset
        except:
            print("Error occoured")
            return HttpResponse("Mistake made")


@api_view(['POST'])
@permission_classes([TeamAdminPermission])
def memberAdd(request):
    addtoGrp(request.data["name"] , request.data["id"])
    return Response(request.data)

