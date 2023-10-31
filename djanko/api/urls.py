from django.urls import  path
from .views import CurrentDateTime,CreateUser,GetUser
urlpatterns = [
    path("test/", CurrentDateTime.as_view()),
    path("sign-up/",CreateUser.as_view()),
    path("get-user-detail/",GetUser.as_view())
    
]