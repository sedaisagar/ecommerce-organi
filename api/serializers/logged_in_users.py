import base64
import hashlib
import hmac
import math
import random
from typing import Union

import requests
from rest_framework import serializers

from cart_orders.models import CartItems, PendingOrder, ShippingBillingAddress
from ecommerce import settings
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
        
        cart_total = CartItems.objects.filter(user=user).aggregate(total=Sum(F('quantity') * F('product__price'))).get("total") or 0
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


class ShippingBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingBillingAddress
        fields = "__all__"

class CartCheckoutSerializer(serializers.Serializer):
    DV = {
        "first_name": "",
        "last_name": "",
        "country": "",
        "street_address": "",
        "apartment_suite_unit": "",  # optional
        "town_city": "",
        "state_country": "",
        "postcode_zip": "",
        "phone": "",
        "email": ""
    }
    payment_method = serializers.ChoiceField(choices=PendingOrder.PAYMENT_METHODS, write_only=True)
    shipping_billing_same = serializers.BooleanField(default=True, write_only=True)

    # Capture Address From Billing In Default
    billing_address = serializers.JSONField(default=DV, write_only=True) 
    shipping_address = serializers.JSONField(default=DV, write_only=True) 


    def inititate_with_khalti(self, validated_data : dict, pending_order: PendingOrder):
        BASE_PATH = "https://dev.khalti.com/api/v2"

        INIT_URL = f"{BASE_PATH}/epayment/initiate/"
        header={
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"  
        }  
        payment_id = random.randint(999,9999999)

        payment_id = f"{pending_order.pk}-{payment_id}".zfill(12)
        pending_order.payment_id = payment_id
        pending_order.save(update_fields=["payment_id"])

        payload = {
            "return_url":"http://localhost:8000/payment-status",
            "website_url":"http://localhost:8000/",
            "amount":str(pending_order.total_amount * 100), # amount in paisa
            "purchase_order_id":payment_id, # Unique id associated with payment	
            "purchase_order_name":f"Payment worth {pending_order.total_amount} by {pending_order.user}"
        }
        response=requests.post(url=INIT_URL,json=payload,headers=header)

        payment_link = ""
        if response.status_code == 200:
            payment_link = response.json().get("payment_url")
        return payment_link

    def initiate_with_esewa(self, validated_data, pending_order:PendingOrder):
        payment_id = random.randint(999,9999999)

        payment_id = f"{pending_order.pk}-{payment_id}".zfill(12)
        pending_order.payment_id = payment_id
        pending_order.save(update_fields=["payment_id"])

        ESEWA_SECRET_KEY = settings.ESEWA_SECRET_KEY
        ESEWA_MERCHANT_ID = settings.ESEWA_MERCHANT_ID

        total_amount = math.trunc(pending_order.total_amount *100 ) / 100

        # input text for signature generation
        input_text = f"total_amount={total_amount},transaction_uuid={payment_id},product_code={ESEWA_MERCHANT_ID}"
        
        # Signature Generation
        hmac_sha256 = hmac.new(ESEWA_SECRET_KEY.encode('utf-8'), input_text.encode('utf-8'), hashlib.sha256)
        digest = hmac_sha256.digest()
        signature = base64.b64encode(digest).decode('utf-8') 

        return {
            "amount":total_amount, 
            "transaction_uuid":payment_id, 
            "product_code":ESEWA_MERCHANT_ID, 
            "signature":signature, 
            "product_code":ESEWA_MERCHANT_ID
        }



    def handle_shipping_billing_address(self, validated_data: dict, pending_order:PendingOrder):
        shipping_billing_same = validated_data.pop("shipping_billing_same", True)

        billing_address : dict = validated_data.pop("billing_address", {})
        shipping_address : dict = validated_data.pop("shipping_address", {})
        
        if shipping_billing_same:
            shipping_billing_serializer = ShippingBillingSerializer(data=billing_address)
            
            valid = shipping_billing_serializer.is_valid(raise_exception=False)
            if not valid:
                raise serializers.ValidationError({
                    "billing_address":shipping_billing_serializer.errors
                })
            
            shipping_billing_instance : ShippingBillingAddress = shipping_billing_serializer.save()
            
            try:
                pending_order.shipping_address.delete()
                pending_order.billing_address.delete()
            except:...

            pending_order.shipping_address = shipping_billing_instance
            pending_order.billing_address = shipping_billing_instance
            pending_order.save(update_fields=["shipping_address", "billing_address"])

        else:
            shipping_serializer = ShippingBillingSerializer(data=shipping_address)
            billing_serializer = ShippingBillingSerializer(data=billing_address)

            svalid = shipping_serializer.is_valid(raise_exception=False) 
            bvalid =  billing_serializer.is_valid(raise_exception=False) 
            
            if not (svalid or bvalid):
                breakpoint()
                raise serializers.ValidationError(
                    {
                        "billing_address": billing_serializer.errors,
                        "shipping_address": shipping_serializer.errors,
                    }
                )

            try:
                pending_order.shipping_address.delete()
                pending_order.billing_address.delete()
            except:...
            
            
            shipping_instance : ShippingBillingAddress = shipping_serializer.save()
            billing_instance : ShippingBillingAddress = billing_serializer.save()
            
            pending_order.shipping_address = shipping_instance
            pending_order.billing_address = billing_instance
            pending_order.save(update_fields=["shipping_address", "billing_address"])
        
        

    def create(self, validated_data: dict):
        # context => {"request":"","view":"", "format":""}
        request = self.context["request"]
        user = request.user
        payment_method = validated_data.pop("payment_method")

        cart_items = CartItems.objects.filter(user=user)
        cart_total = cart_items.aggregate(total=Sum(F('quantity') * F('product__price'))).get("total") or 0

        pending_order = PendingOrder.objects.filter(user=user).first()

        if not pending_order:
            pending_order = PendingOrder.objects.create(
                user = user,
                delivery_charge = 0, 
                coupon_amount = 0,
                payment_method = payment_method,
                total_amount = cart_total,
            )
            pending_order.items.set(cart_items,clear=True)
        else:
            pending_order.total_amount = cart_total
            pending_order.save(update_fields=["total_amount"])
            pending_order.items.set(cart_items,clear=True)
            
        self.handle_shipping_billing_address(validated_data, pending_order)


        match payment_method:
            case "Khalti":
                payment_link = self.inititate_with_khalti(validated_data, pending_order)
                return {
                    "payment_link": payment_link,
                }
            case "Esewa":
                payment_data = self.initiate_with_esewa(validated_data, pending_order)
                return payment_data
            case "COD":
                ...


        return validated_data

    def to_representation(self, instance : dict):
        return instance