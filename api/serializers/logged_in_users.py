from rest_framework import serializers

from cart_orders.models import CartItems
from products.models import Product

class CartActionSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(default=0)

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
                pass

            else:
                # Update Cart
                pass
        else:

            if quantity != 0:
                # Insert to cart
                pass
            else:

                raise serializers.ValidationError({"quantity":"Quantity should be greater than 0 to add item into cart!"})

        return validated_data 