from rest_framework import permissions
from Backend.models import Team

class TeamAdminPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        id_given = request.query_params.get("req_id")
        teamname = request.query_params.get("name")
        team = Team.objects.filter(name=teamname)
        if not team:
            raise Exception("Team doesn't exist")
        else:
            team = team.filter(admin_id=id_given)
            if not team:
                raise Exception("Don't have access")
            else:
                return True

            