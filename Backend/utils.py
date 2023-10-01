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

def GetSlot(duration , amenity_id):
    amenity = Amenity.objects.filter(id=amenity_id)
    x = amenity.first()
    x = x.freeslots.all()
    empty = []
    for i in range(len(x)):
        empty.append(x[i].id)
    full = []
    temp = duration / 15
    booking=[]
    count = 0
    prev = empty[0] - 1
    for item in empty:
        if count == temp:
            print("Slot exists")
            full.append(booking)
            for item in booking:
                empty.remove(item)
            return ({convertIntoTime(booking[0]-1)} , {convertIntoTime(booking[len(booking)-1])})
        if item - prev == 1:
            count += 1
            booking.append(item)
        else:
            count = 0
            booking = []
            
        prev = item
    if count == temp:
        full.append(booking)
        for item in booking:
            empty.remove(item)
        return ({convertIntoTime(booking[0]-1)} , {convertIntoTime(booking[len(booking)-1])})
    else:
        return -1
    



def setInitialFreeSlots():
    amenity = Amenity.objects.filter(id=1)
    # for item in amenity:
    #     if(not item.freeslots.contains(96)):
    #         item.freeslots = [i for i in range(1,97)]
    #     item.save()
    for i in range(1,97):
        amenity[0].freeslots.add(i)
    amenity[0].save()
    # for i in range(1,97):
    #     number = numbers()
    #     number.id = i
    #     number.save()
    