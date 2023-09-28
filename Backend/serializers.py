from Backend.models import User,Group,Team
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'name' , 'enroll_number']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id" , "name"]

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id" , "name" , "members_id" , "admin_id"]