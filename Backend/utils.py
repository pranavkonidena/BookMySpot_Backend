from Backend.models import User,Group,Team,Amenity,IndividualBooking
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


def GetSlot(duration  ,*args, **kwargs):
    duration = int(duration)
    scaled_duration = int(duration/15)
    duration = int(duration)
    scaled_duration = int(duration/15)
    if('location' in kwargs and 'amenity' in kwargs):
        amenity = Amenity.objects.filter(venue=kwargs["location"])
        print(f"GET{len(amenity)}")
        amenity = amenity.filter(name=kwargs["amenity"])
        print(f"GET{len(amenity)}")
    elif('amenity' in kwargs):
        amenity = Amenity.objects.filter(name=kwargs["amenity"])
    elif("location" in kwargs):
        amenity =  Amenity.objects.filter(venue=kwargs["location"])
    if(not 'location' in kwargs and not 'amenity' in kwargs):
        amenity = Amenity.objects.all()
    full_final_times_with_id = []
    for j in range(len(amenity)):
        empty = []
        x = amenity[j]
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
    temp_data = requests.post('https://channeli.in/open_auth/token/?' , data=post_data)
    temp_data = temp_data.json()
    access_token = temp_data["access_token"]
    header = {
        "Authorization" : f"Bearer {access_token}"
    }
    person_data = requests.get('https://channeli.in/open_auth/get_user_data/' , headers=header)

    return person_data.json()
    
def invconvertTime(start_time , end_time):
    first_as_list = start_time.split(":")
    start_hour = int(first_as_list[0])
    start_minute = int(first_as_list[1])

    second_as_list = end_time.split(":")
    end_hour = int(second_as_list[0])
    end_minute = int(second_as_list[1])

    start_hour -= 8
    start_minute /= 15

    start_ans = int(4*start_hour + start_minute)

    end_hour -= 8
    end_minute /= 15

    end_ans = int(4*end_hour + end_minute)


    return f"{start_ans} , {end_ans}"

def invconvertTimeSingle(start_time):
    start_hour = start_time.hour
    start_minute = start_time.minute

    start_hour -= 8
    start_minute /= 15

    start_ans = int(4*start_hour + start_minute)

    return f"{start_ans}"

def makeIndiRes(id_user,amenity_id,start_time,end_time):
    result = invconvertTime(start_time,end_time)
    result_list = result.split(",")
    start = int(result_list[0])
    end = int(result_list[1])

    amenity = Amenity.objects.get(id=amenity_id)
    duration_slot = int((end-start)*15)
    if(start == 0):
        for i in range(start,end+1):
            amenity.freeslots.remove(i)
        amenity.save()
    else:
        for i in range(start+1,end+1):
            amenity.freeslots.remove(i)
        amenity.save()


    booking = IndividualBooking()
    booking.amenity_id=amenity_id
    booking.booker_id=id_user
    booking.time_of_slot = convertIntoTime(start)
    booking.duration_of_booking = duration_slot

    booking.save()

    data = {}
    data["amenity_id"] = amenity_id
    data["booker_id"] = id_user
    data["time_of_slot"] = convertIntoTime(start)
    data["duration_of_booking"] = duration_slot
    data["id"] = booking.id
    return data

def cancelIndiRes(booking_id):
    booking = IndividualBooking.objects.filter(id=booking_id)
    amenity_id = booking[0].amenity.id
    start_time = booking[0].time_of_slot
    duration_of_time = booking[0].duration_of_booking
    start_conv = int(invconvertTimeSingle(start_time))
    end_conv = start_conv + int(int(duration_of_time)/15)
    amenity = Amenity.objects.get(id=amenity_id)
    print(len(amenity.freeslots.all()))
    for i in range(start_conv,end_conv+1):
        if(i not in amenity.freeslots.all()):
            amenity.freeslots.add(i)
    booking.delete()
    amenity.save()

   
