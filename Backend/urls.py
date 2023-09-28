from django.urls import path 
from Backend import views,group_views

urlpatterns = [
    path("user" , views.SpecificUser.as_view()),
    path("group" , group_views.GroupList.as_view()),
    path("group/add" , group_views.memberAdd),
]
