from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from mail_templated import send_mail

from .serializers import (RegisterSerializer, CustomTokenObtainPairSerializer,
                          ChangePasswordSerializer, ProfileSerializer, AuthTokenSerializer)
from accounts.models import Profile



class Home(APIView):
    def get(self, request):
        return Response({
            'detail': 'hi'
        })


class RegisterApi(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            data = {
                'username': serializer.validated_data['username'],
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


class DestroyToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({
            'detail': 'Token destroyd and you logout!'
        },
            status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self, *args, **kwargs):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password for user
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'error': "Old Password is not correct!!"}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()

            return Response({'detail': 'Password Changed Successfully!'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.queryset
        obj = get_object_or_404(queryset, user=self.request.user)

        return obj


class Email(APIView):
    def get(self, request, *args, **kwargs):
        send_mail('email/hello.tpl', {'name': 'Reza'}, 'from_email', ['example@gmail.com'])
        return Response({
            'detail': 'sent'
        })
