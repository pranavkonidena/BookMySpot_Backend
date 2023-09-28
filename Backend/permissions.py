from rest_framework import permissions

class TeamAdminPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        id_given = request.query_params.get("name")
        if(id_given == 'Pranav'):
            return True
        else:
            return request.method == "GET"
            