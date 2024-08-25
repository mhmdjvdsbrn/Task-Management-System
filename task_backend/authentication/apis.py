from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from task_backend.users.models import BaseUser
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

class JWTLoginView(APIView):
    class AuthenticationSerializer(serializers.Serializer):
        phone = serializers.CharField(max_length=11)  
        password = serializers.CharField(required=False) # required is false -> 2-step for login 

    @extend_schema(request=AuthenticationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.AuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')

        try:
            user = BaseUser.objects.get(phone=phone)

            # Use the custom hasher during authentication
            authenticated_user = authenticate(request=request, username=phone, password=password)

            if user and authenticated_user:
                refresh = RefreshToken.for_user(authenticated_user)
                access_token = AccessToken.for_user(authenticated_user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'The user exists. Either you did not enter the password or you entered it incorrectly'},
                                status=status.HTTP_401_UNAUTHORIZED)

        except BaseUser.DoesNotExist:
            return Response({"detail": "User not registered with this phone number"}, status=status.HTTP_404_NOT_FOUND)

class JWTLogoutView(APIView):
    @extend_schema(responses={200: None})
    def post(self, request, *args, **kwargs):
        # For simplicity, assuming the user is authenticated
        logout(request)
        return Response(status=status.HTTP_200_OK)
