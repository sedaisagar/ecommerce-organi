from rest_framework import viewsets, views

from api.serializers.users import UserSerializer
from users.models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse

from utils.permissions import IsAdminUser

from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response


@extend_schema(tags=["User APIs"])
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=["LoggedIn User API(s)"])
class LoggedInUserProfile(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user : User = request.user
        # user = User.objects.all()
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)