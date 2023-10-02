from Backend.models import User,Group,Team,IndividualBooking,Amenity
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

class IndividualBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualBooking
        fields = ["id" , "booker_id" , "time_of_slot" , "duration_of_booking" , "timestamp_of_booking" , "amenity_id"]

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["name" , "id" , "allowed" , "venue" , "freeslots" , "start_time" , "end_time"]

class TimeSerializer(serializers.Serializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    amenity_id = serializers.IntegerField()


