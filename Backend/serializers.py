from Backend.models import User,Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'name' , 'enroll_number']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id" , "name"]