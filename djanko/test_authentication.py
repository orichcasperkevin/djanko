from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt

from django.test import TestCase
from .hanko import authenticate
from base64 import urlsafe_b64encode

        
class DummyPyJWKClient(): 
    """
        Simulate an openID sever,return a JWK
    """
    def convert_to_jwk(self,public_key):
        jwk = {
            "kty": "RSA",
            "kid": "my-key-id",  # Key ID (set to your choice)
            "e": urlsafe_b64encode(public_key.public_numbers().e.to_bytes(4, 'big')).rstrip(b'=').decode('utf-8'),
            "n": urlsafe_b64encode(public_key.public_numbers().n.to_bytes((public_key.public_numbers().n.bit_length() + 7) // 8, 'big')).rstrip(b'=').decode('utf-8')
        }
        return jwk

    def get_signing_key_from_jwt(self,_) :
               
        with open('jwt-key.pub.pem', 'rb') as file:
            public_key_data = file.read()
            public_key = serialization.load_pem_public_key(
                public_key_data, 
                backend=default_backend(),                       
            )                      
        jwk = self.convert_to_jwk(public_key)        
        pyjwt_jwk = jwt.PyJWK(jwk) #convert to pyJWK

        return pyjwt_jwk

class AuthenticationTestCase(TestCase):
    def test_authenticates_token(self):
        def generate_token():   
            with open('jwt-key','rb') as file:
                private_key = file.read()      
                encoded_data = jwt.encode(
                    payload={"name": "Djanko","aud":"localhost"},
                    key=private_key,
                    algorithm="RS256"
                )

            return encoded_data
        token = generate_token()
        valid,data = authenticate(token,DummyPyJWKClient())
        self.assertEqual(valid,True) 
        self.assertEqual(data,{'name': 'Djanko', 'aud': 'localhost'})           