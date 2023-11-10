from django.db import models
import uuid
import datetime
from datetime import time, date, timedelta

# Create your models here.

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=255)
    enroll_number = models.IntegerField()
    profile_pic = models.CharField(max_length=500)
    branch = models.CharField(max_length=255)
    credits = models.IntegerField(default=50)

class Group(models.Model):
    member = models.ManyToManyField("User",related_name="groups" , blank=True)
    name = models.CharField(max_length=255 , verbose_name="name")


class IndividualBooking(models.Model):
    booker = models.ForeignKey("User" , on_delete=models.CASCADE)
    time_of_slot = models.DateTimeField()
    duration_of_booking = models.IntegerField(default=60)
    timestamp_of_booking = models.DateTimeField(auto_now_add=True)
    amenity = models.ForeignKey("Amenity" , on_delete=models.CASCADE)

class GroupBooking(models.Model):
    booker = models.ForeignKey("Group" , on_delete=models.CASCADE)
    time_of_slot = models.DateTimeField()
    duration_of_booking = models.IntegerField(default=60)
    timestamp_of_booking = models.DateTimeField(auto_now_add=True)
    amenity = models.ForeignKey("Amenity" , on_delete=models.CASCADE)
    


class Amenity(models.Model):
    name = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    admin = models.ForeignKey("ModUser", on_delete=models.CASCADE)
    start_time = models.TimeField(default=time(8, 0))
    end_time = models.TimeField(default=time(22, 0))
    credits = models.IntegerField(default=5)
    
class Team(models.Model):
    #Team ID will be automatically generated
    name = models.CharField(max_length=255)
    admin_id = models.ManyToManyField("User" , related_name="Admin")
    members_id = models.ManyToManyField("User" , related_name= "team")
    chats = models.ManyToManyField("Message")


class Event(models.Model):
    amenity = models.ForeignKey(
        "Amenity",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    time_of_occourence_start = models.DateTimeField()
    time_of_occourence_end = models.DateTimeField()
    team = models.ManyToManyField("Team")

class Message(models.Model):
    sender = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_created=True)
    message = models.CharField(max_length=1000)


class ModUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=50 , null=True)
    password = models.CharField(max_length=255, null=True)

class numbers(models.Model):
    value = models.PositiveIntegerField()

class freeSlots(models.Model):
    amenity = models.ForeignKey("Amenity" , on_delete=models.CASCADE , null=True)
    date = models.DateField(primary_key=True)
    slots = models.ManyToManyField("numbers")

class ValidEmails(models.Model):
    email = models.EmailField(max_length=50,unique=True)