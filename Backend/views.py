from Backend.models import User
from Backend.serializers import UserSerializer
from rest_framework import generics
from Backend.utils import create_user
from django.http import HttpResponse
from rest_framework.response import Response
# Create your views here.

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SpecificUser(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        try:
            queryset = User.objects.all()
            uid = self.request.query_params.get('id')
            if uid is not None:
                queryset = queryset.filter(id=uid)
            return queryset
        except:
            print("Error occoured")
            return HttpResponse("Mistake made")



           
