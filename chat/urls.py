from django.urls import path
import chat.views as views
urlpatterns = [
    path("test" , views.TestView.as_view())
]
