'''from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from .models import BlacklistedAccessToken
import re



class TokenValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization') # acess and refresh
        if auth_header:
            try:
                token = auth_header.split(' ')[1] 
                # access_token_obj = AccessToken(token)
                print("token:", token)
                
                # Check if the access token is blacklisted
                if BlacklistedAccessToken.objects.filter(token=token).exists():
                    return JsonResponse({'detail': '---> Invalid token --> .'}, status=401)
                print("Hoke")
            except Exception:
                return JsonResponse({'detail': '=== Invalid token.'}, status=401)
        return None
'''

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from .models import BlacklistedAccessToken


class TokenValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')  # acess and refresh
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                # access_token_obj = AccessToken(token)
                print("token: ", token)

                # Check if the access token is blacklisted
                try:
                    if BlacklistedAccessToken.objects.filter(token=token).exists():
                        return JsonResponse({'detail': 'Invalid token.'}, status=401)
                except Exception as e:
                    print("-----")
                    print(e)



            except Exception:
                return JsonResponse({'detail': '** Invalid token.'}, status=401)
        return None