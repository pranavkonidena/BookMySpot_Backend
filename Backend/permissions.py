from rest_framework import permissions
from Backend.models import Team,ModUser
from rest_framework.exceptions import APIException
class TeamAdminPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if(request.method == "POST"):
            id_given = request.data.get("id")
            teamname = request.data.get("name")
            team = Team.objects.filter(name=teamname)
            if not team:
                raise APIException("Team doesn't exist")
            else:
                team = team.filter(admin_id=id_given)
                if not team:
                    raise APIException("User not admin of team")
                else:
                    return True



class AmenityHeadPermisson(permissions.IsAdminUser):
    def has_permission(self, request, view):
        token = request.data["id"]
        me = ModUser.objects.get(id=token)
        if(me != None):
            return True
        else:
            raise APIException("User is not admin")
