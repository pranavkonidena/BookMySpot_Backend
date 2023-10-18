from django.urls import path 
from Backend import views,group_views,team_views,amenityhead_views

urlpatterns = [
    path("user" , views.SpecificUser.as_view()),
    path("user/auth" , views.userAuth),
    path("user/auth/get" , views.getuserAuth),
    path("user/auth/redirect" , views.redirectuserAuth),
    path("user/getBooking" , views.getBooking),
    path("group" , group_views.GroupList.as_view()),
    path("group/add" , group_views.memberAdd),
    path("team" , team_views.TeamListView.as_view()),
    path("team/create" , team_views.createTeamView),
    path("team/add" , team_views.addMember),
    path("booking/individual" , views.getBooking),
    path("booking/getSlots" , views.getAvailableSlots),
    path("booking/individual/bookSlot" , views.makeIndiReservation),
    path("booking/individual/cancelSlot" , views.cancelIndiReservation),
    path("booking/group/bookSlot" , group_views.groupReservationView),
    path("amenity/head/auth" , amenityhead_views.HeadAuth),
    path("amenity/getAll" , views.AmenitiesList.as_view()),
    path("amenity/head/makeEvent" ,amenityhead_views.CreateEventView),
    path("amenity/head/setSlots" ,amenityhead_views.setSlotsView),
    path("event/register" , team_views.makeTeamReservation),
    path("event/cancel" , team_views.CancelTeamReservation),
    path("event/getSlots" , views.EventsList.as_view()),
]   
