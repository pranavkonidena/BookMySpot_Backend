from Backend.models import User,Group,Team,Amenity,numbers
from rest_framework.exceptions import APIException
import datetime
def create_user(name , enrollnum):
    user = User()
    user.name = name
    user.enroll_number = enrollnum
    user.save()


def addtoGrp(grpname , memberID):
    group = Group()
    allgrps = Group.objects.filter(name = grpname)
    if(not allgrps):
        group.name = grpname
        group.save()
        for item in memberID:
            group.member.add(item)
        group.save()
    else:
        for item in memberID:
            allgrps[0].member.add(item)
        allgrps[0].save()

def createTeam(teamname , admin_id):
    team = Team()
    team.name = teamname
    team.save()
    team.admin_id.add(admin_id)
    team.save()

def addMemberToTeam(teamname , member , admin):
    team = Team.objects.filter(name = teamname)
    if(not team):
        raise APIException("Team not found")
    else:
        if admin == "True":
            team[0].admin_id.add(member)
        else:
            team[0].members_id.add(member)
    team[0].save()

def getAvailableSlots(name , duration , venue , time):
    amenity = Amenity.objects.all()
    if(name != ""):
        amenity = Amenity.objects.filter(name=name)
    if(venue != ""):
        amenity = Amenity.objects.filter(venue=venue)
    if(time != ""):
        amenity = Amenity.objects.filter(freeslots=time)
    
    #idea is every hrs into minutes and then maintain bool for each
    #better version in list of tuples
    #or another idea is store it in array (start array , end array , i , i+1)
    #notify that amenity is empty





import math
def convertIntoTime(a):
    a = a*15
    hours = math.floor(a / 60)
    a = a - (60*hours)
    minutes = a 
    hours = hours+8
    return datetime.time(hour=hours,minute=minutes)

all_bookings = []

empty = []
def GetSlot(duration ,*args, **kwargs):
    duration = int(duration)
    amenity = ""
    scaled_duration = int(duration/15)
    if('location' in kwargs):
        amenity = Amenity.objects.filter(venue=kwargs["location"])
    elif('amenity' in kwargs):
        amenity = Amenity.objects.filter(name=kwargs["amenity"])
    else:
        amenity = Amenity.objects.all()
    full_final_times_with_id = []
    for j in range(len(amenity)):
        x = amenity[j]
        print(x.name)
        x = x.freeslots.all()
        for i in range(len(x)):
            empty.append(x[i].id)
        count=0
        booking = []
        all_booking = []
        prev = empty[0]-1
        for item in empty:
            if(item-prev==1):
                count += 1
                booking.append(item)
            else:
                if count < scaled_duration:
                    count = 1
                    booking = []
                    booking.append(item)
                else:
                    count = 1
                    all_booking.append(booking)
                    booking = []
                    booking.append(item)
            prev = item
        if(len(booking) >= scaled_duration):
            all_booking.append(booking)
        
        final_booking = []
        for item in all_booking:
            if(len(item) > scaled_duration):
                for element in item:
                    if element+scaled_duration-1 in item:
                        temp = []
                        for i in range(int(element),int(element+scaled_duration)):
                            temp.append(i)
                        final_booking.append(temp)
            else:
                final_booking.append(item)


        final_times = []
        for item in final_booking:
            timestamp = (convertIntoTime(item[0]-1) , convertIntoTime(item[len(item)-1]))
            final_times.append(timestamp)
        entry = {}
        entry["id"] = amenity[j].id
        entry["free_slots"] = final_times
        full_final_times_with_id.append(entry)
    return full_final_times_with_id    
    



def setInitialFreeSlots():
    amenity = Amenity.objects.filter(id=2)
    # for item in amenity:
    #     if(not item.freeslots.contains(96)):
    #         item.freeslots = [i for i in range(1,97)]
    #     item.save()
    for i in range(1,57):
        amenity[0].freeslots.add(i)
    amenity[0].save()
    # for i in range(1,57):
    #     number = numbers()
    #     number.id = i
    #     number.save()

import os
import requests
from dotenv import load_dotenv
load_dotenv()

def doOauth(code):
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    redirect_uri = os.environ.get("REDIRECT_URI")
    post_data = {
        "client_id" : client_id,
        "client_secret" : client_secret,
        "grant_type" : "authorization_code",
        "redirect_uri" : redirect_uri,
        "code" : code
    }
    print(f"Code {code}")
   
    temp_data = requests.post('https://channeli.in/open_auth/token/?' , data=post_data)
    temp_data = temp_data.json()
    access_token = temp_data["access_token"]
    header = {
        "Authorization" : f"Bearer {access_token}"
    }
    person_data = requests.get('https://channeli.in/open_auth/get_user_data/' , headers=header)

    return person_data.json()
    

