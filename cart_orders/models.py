from django.db import models

from utils.models import CommonModel

class CartItems(CommonModel):
    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("products.Product",on_delete=models.CASCADE, related_name="cart_items")

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_items"


class PendingOrder(CommonModel):
    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name="pending_orders")
    coupon_code = models.ForeignKey("products.CouponCode", related_name="pending_orders", on_delete=models.CASCADE)
    
    items = models.ManyToManyField(CartItems, related_name="pending_orders", blank=True)

    # Delivery Charge
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Discount Amount
    coupon_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Capture payment information
    payment_id = models.CharField(max_length=45, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    

    class Meta:
        db_table = "pending_order"
     











