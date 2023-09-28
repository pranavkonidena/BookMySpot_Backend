from Backend.models import User,Group,Team
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
    # if(not allteams):
    #     team.name = teamname
    #     team.save()
    #     team.admin_id.add(admin_id)
    #     team.save()
    # else:
    #     raise Exception()

def addMemberToTeam(teamname , member , admin):
    team = Team.objects.filter(name = teamname)
    if(not team):
        raise Exception()
    else:
        if admin == "True":
            team[0].admin_id.add(member)
        else:
            team[0].members_id.add(member)
