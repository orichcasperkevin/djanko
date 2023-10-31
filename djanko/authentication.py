from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from .hanko import authenticate

User = get_user_model()

def deny(reason):
    raise exceptions.AuthenticationFailed(str(reason))

def extract_token_from_header(header: str) -> str:
    parts = header.split()
    return parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else None

class HankoAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):        
        authorization = request.headers.get("Authorization")
        if not authorization:
            return None

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

        try:
            user = User.objects.get(hankoprofile__hanko_id = hanko_id)
        except User.DoesNotExist:
            deny('No such user')        
        return (user, None)