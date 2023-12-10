from rest_framework import permissions,status
from Backend.models import Team,ModUser
from rest_framework.exceptions import APIException
class TeamAdminPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if(request.method == "POST" or request.method == "DELETE"):
            id_given = request.data.get("id")
            team_id = request.data.get("team_id")
            team = Team.objects.filter(id=team_id)
            if not team:
                print(team_id)
                raise APIException("Team doesn't exist")
            else:
                team = team.filter(admin_id=id_given)
                if not team:    
                    raise APIException("User not admin of team")
                else:
                    return True



class AmenityHeadPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        token = request.data.get("token")
        if(request.method == "GET"):
            raise APIException("Get not allowed")
        else:
            token = request.data["token"]
            me = ModUser.objects.filter(id=token).exists()
            if(me):
                return me
            else:
                raise APIException("Not admin")