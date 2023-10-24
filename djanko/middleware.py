import ssl
from django.conf import settings
from django.http import JsonResponse
import jwt

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    
    def _deny(self):
        return JsonResponse({"error": "Unauthorized"},safe=False,status=401)


    def _extract_token_from_header(self,header: str) -> str:
        parts = header.split()
        return parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else None


    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        authorization = request.headers.get("authorization")

        if not authorization:
            return self._deny()

        token = self._extract_token_from_header(authorization)               
        if not token:
            return self._deny()

        try:
            # Disable SSL certificate verification while in development. Don't forget to remove this when in prod
            ssl_context = ssl.create_default_context()
            if settings.DEBUG:  
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE        
            jwks_client = jwt.PyJWKClient(
                settings.HANKO_API_URL + "/.well-known/jwks.json",
                ssl_context=ssl_context
            )          
            token = token + "====" #add padding to token for base64
            signing_key = jwks_client.get_signing_key_from_jwt(token)        
            data = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience="localhost",
            )

            if not data:
                    return self._deny()           

        except (jwt.DecodeError, Exception) as e:
            print(f"Authentication error: {e}")
            return self._deny()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response