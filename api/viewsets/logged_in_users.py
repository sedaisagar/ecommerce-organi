from rest_framework import generics

from api.serializers.logged_in_users import CartActionSerializer
from cart_orders.models import CartItems

from drf_spectacular.utils import extend_schema

from utils.permissions import IsUser

@extend_schema(tags=["LoggedIn User API(s)"])
class UserCartAction(generics.CreateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = CartActionSerializer
    permission_classes = [IsUser]


