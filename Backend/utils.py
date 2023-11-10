from Backend.models import User,Group,Team,Amenity,IndividualBooking,ModUser,freeSlots,GroupBooking,Event,numbers
from rest_framework.exceptions import APIException
import datetime
def create_user(name , enrollnum):
    user = User()
    user.name = name
    user.enroll_number = enrollnum
    user.save()

import json
def addtoGrp(grpname , memberID):
    memberID = json.loads(memberID)
    group = Group()
    allgrps = Group.objects.filter(name = grpname)
    if(not allgrps):
        group.name = grpname
        group.save()
        for item in memberID:
            group.member.add(item)
        group.save()
        return group.id
    else:
        for item in memberID:
            allgrps[0].member.add(item)
        allgrps[0].save()
        return allgrps[0].id
    

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

def removeMemberFromTeam(team_name , member):
    team = Team.objects.filter(name=team_name)
    if(not team):
        raise APIException("Team not found")
    else:
        user = User.objects.get(id=member)
        team[0].members_id.remove(user)
    team[0].save()
    
import math
def convertIntoTime(a):
    a = a*15
    hours = math.floor(a / 60)
    a = a - (60*hours)
    minutes = a 
    hours = hours+8
    return datetime.time(hour=hours,minute=minutes)

all_bookings = []

from datetime import timedelta


def GetSlot(duration ,date ,*args, **kwargs):
    duration = int(duration)
    scaled_duration = int(duration/15)
    duration = int(duration)
    scaled_duration = int(duration/15)
    if('location' in kwargs and 'amenity' in kwargs):
        amenity = Amenity.objects.filter(venue=kwargs["location"])
        print(f"GET{len(amenity)}")
        amenity = amenity.filter(id=kwargs["amenity"])
        print(f"GET{len(amenity)}")
    elif('amenity' in kwargs):
        amenity = Amenity.objects.filter(id=kwargs["amenity"])
        print(len(amenity))
    elif("location" in kwargs):
        amenity =  Amenity.objects.filter(venue=kwargs["location"])
    if(not 'location' in kwargs and not 'amenity' in kwargs):
        amenity = Amenity.objects.all()
    full_final_times_with_id = []
    for j in range(0,len(amenity)+1):
        empty = []
        x = freeSlots.objects.filter(amenity_id=amenity[j].id)
        for i in range(len(x)):
            if(x[i].date.year == date.year and x[i].date.month==date.month and x[i].date.day==date.day):
                empty.append(x[i].slots.all())
        if(len(empty) == 0):
            return []
        else:     
            count=0
            booking = []
            all_booking = []
            for item in empty:
                prev = item[0].value-1
                for i in range(len(item)):
                    if(item[i].value-prev==1):
                        count += 1
                        booking.append(item[i].value)
                    else:
                        if count < scaled_duration:
                            count = 1
                            booking = []
                            booking.append(item[i].value)
                        else:
                            count = 1
                            all_booking.append(booking)
                            booking = []
                            booking.append(item[i].value)
                    prev = item[i].value
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

                current_date = datetime.date(datetime.datetime.today().year , datetime.datetime.today().month , datetime.datetime.today().day)
                final_times = []
                print(current_date)
                if(current_date.day == date.day):
                    for item in final_booking:
                        print("U R REQUESTING TOFSYQ!!!")
                        if((datetime.datetime.now()+timedelta(hours=11,minutes=30)).time() < convertIntoTime(item[0]-1)):
                            timestamp = (convertIntoTime(item[0]-1) , convertIntoTime(item[len(item)-1]))
                            final_times.append(timestamp)
                else:
                    print("U DIDNT CALL ")
                    for item in final_booking:
                        timestamp = (convertIntoTime(item[0]-1) , convertIntoTime(item[len(item)-1]))
                        final_times.append(timestamp)
                entry = {}
                entry["id"] = amenity[j].id
                entry["free_slots"] = final_times
                full_final_times_with_id.append(entry)
            return full_final_times_with_id    
                
import os
import requests
from dotenv import load_dotenv
load_dotenv()

from Backend.models import User

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
    temp_data = requests.post('https://channeli.in/open_auth/token/' , data=post_data)
    if(temp_data.status_code != 200):
        raise Exception()
    temp_data = temp_data.json()
    access_token = temp_data["access_token"]
    header = {
        "Authorization" : f"Bearer {access_token}"
    }
    person_data = requests.get('https://channeli.in/open_auth/get_user_data/' , headers=header)
    if(person_data.status_code != 200):
        raise Exception()
    person_data = person_data.json()
    enrollNum = person_data["username"]
    name = person_data["person"]["fullName"]
    display_pic = person_data["person"]["displayPicture"]
    branch_name = person_data["student"]["branch name"]
    user = User()
    try:
        user_exists = User.objects.get(enroll_number=enrollNum)
        return user_exists.id
    except:
        user.enroll_number = enrollNum
        user.name = name
        if(display_pic == None):
            user.profile_pic = "https://github-production-user-asset-6210df.s3.amazonaws.com/122373207/275466089-4e5a891c-8afd-4e9b-a0da-04ff0c39687c.png"
        else:
            user.profile_pic = display_pic
        user.branch = branch_name
        user.save()
        return user.id

    
    
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

def makeIndiRes(id_user,amenity_id,start_time,end_time,date):
    result = invconvertTime(start_time,end_time)
    result_list = result.split(",")
    start = int(result_list[0])
    end = int(result_list[1])
    duration_slot = int((end-start)*15)
    x = freeSlots.objects.filter(amenity_id=amenity_id)
    u = User.objects.get(id=id_user)
    u.credits = u.credits - Amenity.objects.get(id=amenity_id).credits
    print(u.credits)
    if(u.credits < 0):
        return -1
    else:
        for i in range(len(x)):
            if(x[i].date.month == date.month and x[i].date.day == date.day and x[i].date.year == date.year):
                if(start == 0):
                    for j in range(start+1,end+1):
                        n = numbers.objects.get(value=j)
                        x[i].slots.remove(n)
                    x[i].save()
                else:
                    for j in range(start+1,end+1):
                        n = numbers.objects.get(value=j)
                        x[i].slots.remove(n)
                    x[i].save()
        u.save()
        booking = IndividualBooking()
        booking.amenity_id=amenity_id
        booking.booker_id=id_user
        booking.duration_of_booking = duration_slot
        slot_time = convertIntoTime(start)
        booking.time_of_slot = datetime.datetime(date.year,date.month,date.day,slot_time.hour,slot_time.minute,0,0)
        booking.save()
        data = {}
        data["amenity_id"] = amenity_id
        data["booker_id"] = id_user
        data["time_of_slot"] = convertIntoTime(start)
        data["duration_of_booking"] = duration_slot
        data["id"] = booking.id
        return data

def cancelGroupRes(booking_id):
    booking = GroupBooking.objects.filter(id=booking_id)
    print(booking)
    amenity_id = booking[0].amenity.id
    start_time = booking[0].time_of_slot
    duration_of_time = booking[0].duration_of_booking
    start_conv = int(invconvertTimeSingle(start_time))
    end_conv = start_conv + int(int(duration_of_time)/15)
    print(f"START_CONV{start_conv}")
    print(f"END_CONV{end_conv}")
    slots = freeSlots.objects.filter(amenity_id=amenity_id)
    for i in range(len(slots)):
        if(slots[i].date.month == start_time.month and slots[i].date.day == start_time.day and slots[i].date.year == start_time.year):
            if start_conv != 0:
                for j in range(start_conv,end_conv+1):
                    if(j not in slots[i].slots.all()):
                        n = numbers.objects.get(value=j)
                        slots[i].slots.add(n)
            else:
                for j in range(start_conv+1,end_conv+1):
                    if(j not in slots[i].slots.all()):
                        n = numbers.objects.get(value=j)
                        slots[i].slots.add(n)

        
        slots[i].save()
    booking.delete()



def cancelIndiRes(booking_id):
    booking = IndividualBooking.objects.filter(id=booking_id)
    print(booking)
    amenity_id = booking[0].amenity.id
    start_time = booking[0].time_of_slot
    duration_of_time = booking[0].duration_of_booking
    start_conv = int(invconvertTimeSingle(start_time))
    end_conv = start_conv + int(int(duration_of_time)/15)
    print(f"START_CONV{start_conv}")
    print(f"END_CONV{end_conv}")
    slots = freeSlots.objects.filter(amenity_id=amenity_id)
    for i in range(len(slots)):
        if(slots[i].date.month == start_time.month and slots[i].date.day == start_time.day and slots[i].date.year == start_time.year):
            if start_conv != 0:
                for j in range(start_conv,end_conv+1):
                    if(j not in slots[i].slots.all()):
                        n = numbers.objects.get(value=j)
                        slots[i].slots.add(n)
            else:
                for j in range(start_conv+1,end_conv+1):
                    if(j not in slots[i].slots.all()):
                        n = numbers.objects.get(value=j)
                        slots[i].slots.add(n)

        
        slots[i].save()
    booking.delete()

   
def AuthForHead(email , password):
    #Check if given email is a valid head email
    me = ModUser.objects.filter(email=email)
    if(len(me) != 0):
        me = me.filter(password=password)
        if(len(me) != 0):
            return me[0].id
        else:
            return False
    else:
        return False
            
    


def groupReservation(group_id , start_time , end_time ,amenity_id,date):
    result = invconvertTime(start_time,end_time)
    result_list = result.split(",")
    start = int(result_list[0])
    end = int(result_list[1])
    
    slots = freeSlots.objects.filter(amenity_id = amenity_id)
    for i in range(len(slots)):
        if(slots[i].date.month == date.month and slots[i].date.day == date.day and slots[i].date.year == date.year):
            slot = slots[i]
    duration_slot = int((end-start)*15)
    if(start == 0):
        for i in range(start+1,end+1):
            n = numbers.objects.get(value=i)
            slot.slots.remove(n)
        slot.save()
    else:
        for i in range(start+1,end+1):
            n = numbers.objects.get(value=i)
            slot.slots.remove(n)
        slot.save()


    booking = GroupBooking()
    booking.amenity_id=amenity_id
    booking.booker_id=group_id
    time_of_slot = convertIntoTime(start)
    booking.duration_of_booking = duration_slot
    booking.time_of_slot = datetime.datetime(date.year,date.month,date.day,time_of_slot.hour , time_of_slot.minute , time_of_slot.second)
    booking.save()

    data = {}
    data["amenity_id"] = amenity_id
    data["booker_id"] = group_id
    data["time_of_slot"] = str(booking.time_of_slot)
    data["duration_of_booking"] = duration_slot
    data["id"] = booking.id
    return data

def checkForEvents(amenity_id):
    events = Event.objects.filter(amenity=amenity_id)
    if(len(events) == 0):
        return False
    else:
        event_times = {}
        item = events[len(events)-1]
        event_times[item.name] = (item.time_of_occourence_start,item.time_of_occourence_end)
        return event_times 

def removeSlotsWhileEvent(amenity_id):
    result = checkForEvents(amenity_id)
    if result == False:
        print("FALSE")
    else:
        for item in result:
            (start_time , end_time) = result[item]
            if(start_time.date() == end_time.date()):
                start_conv = int(invconvertTimeSingle(start_time))
                end_conv = int(invconvertTimeSingle(end_time))
                fe = freeSlots.objects.filter(amenity_id=amenity_id)
                fe = fe.get(date=start_time.date())
                for i in range(start_conv+1,end_conv+1):
                    n = numbers.objects.get(value=i)
                    if n in fe.slots.all():
                        fe.slots.remove(n)
                fe.save()
            else:
                start_conv = int(invconvertTimeSingle(start_time))
                end_conv = int(invconvertTimeSingle(end_time))
                #First remove all slots from start_conv to end then from start to end_conv
                fe = freeSlots.objects.filter(amenity_id=amenity_id)
                current_date = start_time.date()
                while(current_date != end_time.date()):
                    fen = fe.get(date=current_date)
                    if current_date == start_time.date():
                        for i in range(start_conv,57):
                            n = numbers.objects.get(value=i)
                            if n in fen.slots.all():
                                fen.slots.remove(n)
                        fen.save()
                    elif(current_date != end_time.date()):
                        fea = fe.get(date=current_date)
                        for i in range(1,57):
                            n = numbers.objects.get(value=i)
                            if n in fea.slots.all():
                                fea.slots.remove(n)
                        fea.save()
                    else:
                        fec=fe.get(date=current_date)
                        for i in range(1,end_conv+1):
                            n = numbers.objects.get(value=i)
                            if(n in fec.slots.all()):
                                fec.slots.remove(n)
                        fec.save()
                    current_date = start_time.date() + datetime.timedelta(days=1)


def createEvent(amenity_id , event_name , time_of_occourence_start , time_of_occourence_end):
    event = Event()
    event.amenity_id = amenity_id
    event.name = event_name
    format ='%Y-%m-%d %H:%M:%S'
    event.time_of_occourence_start = datetime.datetime.strptime(time_of_occourence_start , format)
    event.time_of_occourence_end = datetime.datetime.strptime(time_of_occourence_end , format)
    event.save()

    removeSlotsWhileEvent(amenity_id)

    data = {}
    data["amenity_id"] = amenity_id
    data["name"] = event_name
    data["time_of_occourence_start"] = time_of_occourence_start
    data["time_of_occourence_end"] = time_of_occourence_end
    data["team"] = []
    return data


def addTeamToEvent(event_id , team_id):
    event = Event.objects.get(id=event_id)
    if not event:
        raise APIException("Event not found")
    else:
        event.team.add(team_id)
    
    event.save()

    return event.team


def cancelTeamReservation(name , event_id):
    team = Team.objects.filter(name=name)
    team_id = team[0].id
    print(team_id)
    events = Event.objects.all()
    print(len(events[0].team.all()))
    match_i = -5
    event = Event.objects.filter(id=event_id)
    event = event.filter(team=team_id)
    for item in event:
        for i in range(len(item.team.all())):
            if(item.team.all()[i].name == name):
                match_i = i
                break
        if match_i >= 0:
            break
    event[0].team.remove(event[0].team.all()[match_i])
    event[0].save()

    


