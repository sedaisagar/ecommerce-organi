from rest_framework import generics, status

from api.serializers.auth import UserRegisterSerializer
from users.models import User

from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Auth"], summary="Login API")
class CustomTokenObtainPairView(TokenObtainPairView):...
@extend_schema(tags=["Auth"], summary="Refresh API")
class CustomTokenRefreshView(TokenRefreshView):...

@extend_schema(tags=["Auth"], summary="User Registration API")
class UserRegisterView(generics.CreateAPIView):
    """
    User can signup to the application using this endpoint
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid(raise_exception=False)
        
        if is_valid:
            self.perform_create(serializer)

            return Response({
                "title":"User Registration", 
                "message":"User Registration Successful!", 
                "success":True,
                "data":serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "title":"User Registration", 
            "message":"User Registration UnSuccessful!", 
            "success":False,
            "errors":serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)