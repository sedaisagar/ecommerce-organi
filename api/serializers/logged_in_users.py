from typing import Union

from rest_framework import serializers

from cart_orders.models import CartItems
from products.models import Product

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