from Backend.models import Team
from Backend.serializers import TeamSerializer
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from Backend.utils import createTeam , addMemberToTeam , addTeamToEvent , cancelTeamReservation , removeMemberFromTeam
from Backend.permissions import TeamAdminPermission
from django.db.models import Q
from rest_framework import status
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
            queryset = queryset.filter(Q(members_id = uid) | Q(admin_id=uid))
        queryset = queryset.distinct()
        return queryset

class TeamListIDView(generics.ListAPIView):
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        queryset = Team.objects.filter(id=self.request.query_params.get("id"))
        return queryset

@api_view(['POST'])
def createTeamView(request):
    teamname = request.data["name"]
    admin_id = request.data["id"]
    teamId = createTeam(teamname , admin_id)
    return Response(teamId)


@api_view(['POST'])
@permission_classes([TeamAdminPermission])
def addMember(request):
    print("GOT")
    if request.method == "POST":
        teamid = request.data["team_id"]
        member_id = request.data["member_id"]
        admin = request.data["admin"]
        print(teamid)
        print(member_id)
        print(admin)
        addMemberToTeam(teamid , member_id , admin)
        return Response(request.data)
    else:
        return Response("OK")

@api_view(['POST'])
@permission_classes([TeamAdminPermission])
def removeMember(request):
    if request.method == "POST":
        team_id = request.data["team_id"]
        member_id = request.data["member_id"]
        removeMemberFromTeam(team_id , member_id)
        return Response("Ok")

@api_view(['POST'])
def exitTeam(request):
    if request.method == "POST":
        team_id = request.data["team_id"]
        member_id = request.data["member_id"]
        try:
            removeMemberFromTeam(team_id , member_id)
            return Response("Ok" , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Error" , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([TeamAdminPermission])
def makeTeamReservation(request):
    data = addTeamToEvent(request.data["event_id"] , request.data["team_id"])
    
    return Response("OK")

@api_view(['POST'])
@permission_classes([TeamAdminPermission])
def CancelTeamReservation(request):
    name = request.data["name"]
    event_id = request.data["event_id"]
    cancelTeamReservation(name , event_id)
    return Response("Ok")

class TeamswithAdmin(generics.ListAPIView):
    serializer_class = TeamSerializer
    def get_queryset(self):
        id = self.request.query_params.get("id")
        queryset = Team.objects.filter(admin_id=id)
        return queryset

@api_view(['DELETE'])
@permission_classes([TeamAdminPermission])
def DeleteTeam(request):
    try:
        id = int(request.data["team_id"])
        team = Team.objects.get(id=id)
        team.delete()
        # team.save()
        return Response("Ok")
    except Exception as e:
        return Response("Error" , status=status.HTTP_500_INTERNAL_SERVER_ERROR)