from rest_framework import generics

from api.serializers.logged_in_users import (
    CartActionSerializer, 
    CartCheckoutSerializer, 
    CouponApplySerializer,
    PaymentVerifySerializer, 
    PendingOrderSerializer,
    ShippingBillingSerializer,
    UserOrdersSerializer,
)
from cart_orders.models import CartItems, PendingOrder, UserOrder

from drf_spectacular.utils import extend_schema

from products.models import CouponCode
from utils.permissions import IsUser
from django.db.models import Sum, F

@extend_schema(tags=["LoggedIn User API(s)"])
class UserCartListAction(generics.ListCreateAPIView):
    queryset = CartItems.objects.all()
    serializer_class = CartActionSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        queryset =  super().get_queryset()
        
        # Filter by specific user who is logged in / authenticated
        queryset = queryset.filter(user=self.request.user)

        return queryset

    def list(self, request, *args, **kwargs):
        # ALL DATA
        qs = self.get_queryset()
        # ALL DATA

        queryset = self.filter_queryset(qs)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        response = self.get_paginated_response(serializer.data)
        
        agg_result = qs.aggregate(
            total = Sum(F('quantity') * F('product__price'))            
        )
        
        total_amount = agg_result.get("total") 
        
        pending_order = PendingOrder.objects.filter(user=self.request.user).first()
        
        if not pending_order:
            response.data["meta"] = {
                "sub_total":total_amount,
                "discount":0,
                "delivery_charge":0,
                "total":total_amount,
            }
        else:
            response.data["meta"] = {
                "pending_order":PendingOrderSerializer(pending_order).data,
                "shipping_address": ShippingBillingSerializer(pending_order.shipping_address).data,
                "billing_address": ShippingBillingSerializer(pending_order.billing_address).data,
            }

        return response

@extend_schema(tags=["LoggedIn User API(s)"])
class CouponApplyView(generics.CreateAPIView):
    queryset = CouponCode.objects.all()
    serializer_class = CouponApplySerializer
    permission_classes = [IsUser]


@extend_schema(tags=["LoggedIn User API(s)"])
class CartCheckoutView(generics.CreateAPIView):
    # queryset = CouponCode.objects.all()
    serializer_class = CartCheckoutSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        return []

@extend_schema(tags=["LoggedIn User API(s)"])
class PaymentVerifyView(generics.CreateAPIView):
    # queryset = CouponCode.objects.all()
    serializer_class = PaymentVerifySerializer
    permission_classes = []

    def get_queryset(self):
        return []

@extend_schema(tags=["LoggedIn User API(s)"])
class UserOrdersView(generics.ListAPIView):
    queryset = UserOrder.objects.all()
    serializer_class = UserOrdersSerializer
    permission_classes = [IsUser]

