from rest_framework import permissions
from Backend.models import Team
from rest_framework.exceptions import APIException

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

            