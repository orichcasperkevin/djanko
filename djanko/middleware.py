from django.http import JsonResponse
from .hanko import authenticate

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    
    def _deny(self,reason):
        return JsonResponse(
            {"error": "Unauthorized " + str(reason)},
            safe=False,status=401
        )


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

        
        valid,data = authenticate(token)
        if not valid:
            return self._deny(data)           
        if valid:
            if not data:
                self._deny("No data in token")
            print(data)
    

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response