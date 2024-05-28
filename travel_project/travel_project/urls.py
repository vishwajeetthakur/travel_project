from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.authentication import JWTAuthentication

from travel_admin import views
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

# class CustomSchemaGenerator(OpenAPISchemaGenerator):
#     def get_security_definitions(self):
#         return {
#             'Bearer': {
#                 'type': 'apiKey',
#                 'name': 'Authorization',
#                 'in': 'header',
#                 'description': 'Enter JWT as `Bearer <token>`'
#             }
#         }

# Use the custom schema generator in your schema view configuration
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Travel Admin API",
#         default_version='v1',
#         description="APIs for managing travel data",
#         terms_of_service="https://www.example.com/policies/terms/",
#         contact=openapi.Contact(email="contact@example.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     authentication_classes=(JWTAuthentication,),
#     permission_classes=(permissions.AllowAny,),
#     generator_class=CustomSchemaGenerator
# )

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 200:
#             token = response.data.get('access')
#             request.session['jwt'] = token  # Store token in session
#         return response

# from travel_admin.views import PatchLogoutView

schema_view = get_schema_view(
    openapi.Info(
        title="Travel Admin API",
        default_version='v1',
        description="APIs for managing travel data",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=(JWTAuthentication,),
    # permission_classes=(AllowAny,),
    permission_classes=(permissions.AllowAny,),
    # Define Security Definition and Security Requirement properly for JWT

)



urlpatterns = [
    path('admin/', admin.site.urls),

    # DRF and drf-yasg URL configurations
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    

    path('', include('travel_admin.urls')), 
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path("api-auth/logout/", views.PatchLogoutView.as_view(), name="new-logout"),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
   
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/logout/', views.LogoutView.as_view(), name ='logout'),
    # path('token/', 
    #       jwt_views.TokenObtainPairView.as_view(), 
    #       name ='token_obtain_pair'),
    #  path('token/refresh/', 
    #       jwt_views.TokenRefreshView.as_view(), 
    #       name ='token_refresh'),

    
]
