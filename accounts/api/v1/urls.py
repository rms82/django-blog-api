# from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path
from .views import (Home, RegisterApi, CustomAuthToken, DestroyToken,
                    CustomTokenObtainPairView, ChangePasswordApiView)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'api-v1'
urlpatterns = [
    path('', Home.as_view()),

    # Register
    path('register/', RegisterApi.as_view(), name='register'),

    # Password
    path('change/password/', ChangePasswordApiView.as_view(), name='change_password'),

    # Profile
    

    # Token Auth
    path('token/login/', CustomAuthToken.as_view(), name='token_login'),
    path('token/logout/', DestroyToken.as_view(), name='token_logout'),

    # JWt Auth
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
]
