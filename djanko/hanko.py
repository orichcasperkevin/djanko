import jwt
import ssl
from django.conf import settings

def padded_token(token):
    padding_needed = len(token) % 4
    if padding_needed:
        padding_needed = 4 - padding_needed
    return token + ('=' * padding_needed)

def authenticate(token:str) -> tuple:
    ssl_context = ssl.create_default_context()
    if settings.DEBUG:  
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE        
    jwks_client = jwt.PyJWKClient(
        settings.HANKO_API_URL + "/.well-known/jwks.json",
        ssl_context=ssl_context
    )                   
    token = padded_token(token) #add padding to token for base64
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)        
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="localhost",
        )
        return (True,data)
    
    except (jwt.DecodeError, Exception) as e:
        return (False,e)
