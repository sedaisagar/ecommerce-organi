from typing import Union

from rest_framework import serializers

from cart_orders.models import CartItems, PendingOrder
from products.models import CouponCode, Product

class CartActionSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    quantity = serializers.IntegerField(default=0, write_only=True)

    # If quantity = 0 , then remove action
    # Else update or create the cart item
    # 

    def create(self, validated_data):
        # IMPLEMENT HERE

        request = self.context["request"]
        user = request.user
        product = validated_data.pop("product")
        quantity = validated_data.pop("quantity")

        exists = CartItems.objects.filter(user=user, product=product).exists()


        if exists:
            
            if quantity == 0:
                # Remove from cart
                CartItems.objects.filter(user=user, product=product).delete()

            else:
                # Update Cart
                CartItems.objects.filter(user=user, product=product).update(quantity=quantity)
        else:

            if quantity != 0:
                # Insert to cart
                CartItems.objects.create(
                    user=user,
                    product=product,
                    quantity=quantity,
                    priority=1
                )
            else:

                raise serializers.ValidationError({"quantity":"Quantity should be greater than 0 to add item into cart!"})

        return {"message":"Operation Success"} 


    def to_representation(self, instance : Union[dict, CartItems]):
        if isinstance(instance, dict):
            return instance
        else:
            # OBJECT RESPONSE
            request = self.context["request"]
            

            return {
                "quantity":instance.quantity,
                "product": {
                    "name":instance.product.name,
                    "price":instance.product.price,
                    "image":request.build_absolute_uri(instance.product.image.url),
                },
                "sub_total":instance.quantity * instance.product.price,
            }

from django.utils.timezone import now
from django.db.models import Sum, F
class CouponApplySerializer(serializers.Serializer):
    coupon_code = serializers.CharField(write_only=True)

    def validate(self, attrs):
        coupon_code = attrs.get("coupon_code")
        if not CouponCode.objects.filter(code=coupon_code).exists():
            raise serializers.ValidationError({"coupon_code":"Coupon code does not exist!"})
        
        if not CouponCode.objects.filter(code=coupon_code, expires_at__gt=now()):
            raise serializers.ValidationError({"coupon_code":"Coupon code is expired or invalid!"})

        return super().validate(attrs)

    def create(self, validated_data):
        coupon_code = validated_data.pop("coupon_code")
        request = self.context["request"]
        user = request.user

        cart_items = CartItems.objects.filter(user=user)
        
        coupon = CouponCode.objects.get(code=coupon_code)
        
        cart_total = CartItems.objects.aggregate(total=Sum(F('quantity') * F('product__price'))).get("total") or 0
        pending_order, _ = PendingOrder.objects.update_or_create(
            user = user,
            defaults=dict(
                coupon_code = coupon, # throws exception if mulitple objects returned
                # items = 
                delivery_charge = 0, 
                coupon_amount = coupon.discount_amount,
                # payment_id = 
                total_amount = cart_total - coupon.discount_amount,
                priority = 1,
            )
        )
        pending_order.items.set(cart_items, clear=True)

        return {"message":"Coupon Applied Successfully!"}

    def to_representation(self, instance):
        return instance


class PendingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingOrder
        # fields = "__all__"
        exclude = ["items", "coupon_code", "user", "id", "publish", "priority"]