from django.urls import  path
from .views import CurrentDateTime,CreateUser
urlpatterns = [
    path("test/", CurrentDateTime.as_view()),
    path("sign-up/",CreateUser.as_view())
    
]