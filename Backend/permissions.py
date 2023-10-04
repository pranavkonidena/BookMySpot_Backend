from rest_framework import permissions
from Backend.models import Team
from rest_framework.exceptions import APIException
from Backend.utils import AuthForHead
class TeamAdminPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
    
        id_given = request.query_params.get("id")
        teamname = request.query_params.get("name")
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
        email = request.query_params.get("email")
        password = request.query_params.get("password")
        result = AuthForHead(email,password=password)
        if result:
            return True
        else:
            raise APIException("User not amenity head")
