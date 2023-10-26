import datetime
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status

from .serializers import UserSerializer

User = get_user_model()


class CreateUser(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        hanko_id = "suiu-wejnkwne-sdjh"    
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(hanko_id=hanko_id)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        }) 

class CurrentDateTime(APIView):
    def get(self,_):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return Response(html,status=status.HTTP_200_OK)