from django.shortcuts import render
from rest_framework import generics
from Backend.models import Message
from Backend.serializers import MessageSerializer
# Create your views here.

class TestView(generics.ListAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
