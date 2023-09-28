from django.db import models
import uuid
# Create your models here.

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=255)
    enroll_number = models.IntegerField()
    profile_pic = models.CharField(max_length=500)


class Group(models.Model):
    member = models.ManyToManyField("User",related_name="groups" , blank=True)
    name = models.CharField(max_length=255 , verbose_name="name")


class IndividualBooking(models.Model):
    booker_id = models.ForeignKey("User" , on_delete=models.CASCADE)
    time_of_slot = models.DateTimeField()
    name_of_slot = models.CharField(max_length=255)
    timestamp_of_booking = models.DateTimeField(auto_now_add=True)
    amenity_id = models.ForeignKey("Amenity" , on_delete=models.CASCADE)

class GroupBooking(models.Model):
    booker_id = models.ForeignKey("Group" , on_delete=models.CASCADE)
    time_of_slot = models.DateTimeField()
    name_of_slot = models.CharField(max_length=255)
    timestamp_of_booking = models.DateTimeField(auto_now_add=True)
    amenity_id = models.ForeignKey("Amenity" , on_delete=models.CASCADE)
    


class Amenity(models.Model):
    name = models.CharField(max_length=255)
    allowed = models.BooleanField()
    venue = models.CharField(max_length=255)
    admin = models.ForeignKey("ModUser" , on_delete=models.CASCADE)

class Team(models.Model):
    #Team ID will be automatically generated
    name = models.CharField(max_length=255)
    admin_id = models.ManyToManyField("User" , related_name="Admin")
    members_id = models.ManyToManyField("User" , related_name= "team")
    chats = models.ManyToManyField("Message")


class Event(models.Model):
    amenity_id = models.ForeignKey(
        "Amenity",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    time_of_occourence_start = models.DateTimeField()
    time_of_occourence_end = models.DateTimeField()


class Message(models.Model):
    sender = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_created=True)
    message = models.CharField(max_length=1000)


class ModUser(models.Model):
    name = models.CharField(max_length=255)