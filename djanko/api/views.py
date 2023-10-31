import datetime
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status

from .serializers import UserSerializer
from ..hanko import authenticate


User = get_user_model()

def deny(reason):
    return JsonResponse(
        {"error": "Unauthorized " + str(reason)},
        safe=False,status=401
    )

def extract_token_from_header(header: str) -> str:
    parts = header.split()
    return parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else None


class CreateUser(GenericAPIView):
    authentication_classes = [] #disables Hanko authentication
    serializer_class = UserSerializer    

    def post(self, request):       
        authorization = request.headers.get("Authorization")
        if not authorization:
            return deny("'Authorization' header was not found")

        token = extract_token_from_header(authorization)               
        if not token:
            return deny('No token')

        valid,token_data = authenticate(token)
        if not valid:
            return deny(token_data)           
        if valid:
            if not token_data:
                deny("No data in token")            
        
        hanko_id = token_data.get('sub')    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(hanko_id=hanko_id)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,

        }) 

class GetUser(APIView):    

    def get(self,request):
        user = request.user
        return Response(
            UserSerializer(user).data
        )


class CurrentDateTime(APIView):
    def get(self,_):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return Response(html,status=status.HTTP_200_OK)