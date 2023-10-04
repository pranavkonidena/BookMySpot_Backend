from Backend.models import Team
from Backend.serializers import TeamSerializer
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from Backend.utils import createTeam , addMemberToTeam , addTeamToEvent
from Backend.permissions import TeamAdminPermission
class TeamListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
       
        queryset = Team.objects.all()
        uid = self.request.query_params.get('id')
        if uid is not None:
            queryset = queryset.filter(members_id = uid)
        return queryset
        

@api_view(['POST'])
def createTeamView(request):
    teamname = request.data["name"]
    admin_id = request.data["id"]
    createTeam(teamname , admin_id)
    return Response(request.data)


@api_view(['GET','POST'])
@permission_classes([TeamAdminPermission])
def addMember(request):
    if request.method == "POST":
        teamname = request.data["name"]
        member_id = request.data["id"]
        admin = request.data["admin"]
        addMemberToTeam(teamname , member_id , admin)
        return Response(request.data)
    else:
        return Response("OK")
import json
@api_view(['POST'])
@permission_classes([TeamAdminPermission])
def makeTeamReservation(request):
    data = addTeamToEvent(request.data["event_id"] , request.data["team_id"])
    return Response("OK")