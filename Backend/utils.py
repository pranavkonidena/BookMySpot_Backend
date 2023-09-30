from Backend.models import User,Group,Team,Amenity
from rest_framework.exceptions import APIException
from logging import log
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
    
    
