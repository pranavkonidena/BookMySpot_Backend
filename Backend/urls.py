from django.urls import path 
from Backend import views,group_views,team_views

urlpatterns = [
    path("user" , views.SpecificUser.as_view()),
    path("group" , group_views.GroupList.as_view()),
    path("group/add" , group_views.memberAdd),
    path("team" , team_views.TeamListView.as_view()),
    path("team/create" , team_views.createTeamView),
    path("team/add" , team_views.addMember)
]
