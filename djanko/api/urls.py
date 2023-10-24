from django.urls import  path
from .views import CurrentDateTime
urlpatterns = [
    path("test/", CurrentDateTime.as_view(), name="test"),
    
]