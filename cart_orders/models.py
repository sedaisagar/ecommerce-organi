from django.db import models

from utils.models import CommonModel

class CartItems(CommonModel):
    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("products.Product",on_delete=models.CASCADE, related_name="cart_items")

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_items"


class ShippingBillingAddress(CommonModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_suite_unit = models.CharField(max_length=100)  
    town_city = models.CharField(max_length=100)
    state_country = models.CharField(max_length=100)
    postcode_zip = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    class Meta:
        db_table = "shipping_billing_address"

class PendingOrder(CommonModel):
    PAYMENT_METHODS = (
        ("Khalti", "Khalti"),
        ("Esewa", "Esewa"),
        ("COD", "COD"),
    )
    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name="pending_orders")
    coupon_code = models.ForeignKey("products.CouponCode", related_name="pending_orders", on_delete=models.SET_NULL, null=True, blank=True)
    
    items = models.ManyToManyField(CartItems, related_name="pending_orders", blank=True)

    # Delivery Charge
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Discount Amount
    coupon_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Capture payment information
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS, default="COD")
    payment_id = models.CharField(max_length=45, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    shipping_address = models.ForeignKey(ShippingBillingAddress, on_delete=models.SET_NULL, related_name="s_pending_orders", null=True, blank=True)
    billing_address = models.ForeignKey(ShippingBillingAddress, on_delete=models.SET_NULL, related_name="b_pending_orders", null=True, blank=True)
    
    class Meta:
        db_table = "pending_order"


class OrderItems(CommonModel):
    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey("products.Product",on_delete=models.CASCADE, related_name="order_items")

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table = "order_items"

class UserOrder(CommonModel):
    PAYMENT_METHODS = (
        ("Khalti", "Khalti"),
        ("Esewa", "Esewa"),
        ("COD", "COD"),
    )
    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name="orders")
    coupon_code = models.ForeignKey("products.CouponCode", related_name="orders", on_delete=models.SET_NULL, null=True, blank=True)
    
    items = models.ManyToManyField(OrderItems, related_name="orders", blank=True)

    # Delivery Charge
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Discount Amount
    coupon_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Capture payment information
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS, default="COD")
    payment_id = models.CharField(max_length=45, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_gateway_data = models.JSONField(default=dict) 

    shipping_address = models.ForeignKey(ShippingBillingAddress, on_delete=models.SET_NULL, related_name="s_orders", null=True, blank=True)
    billing_address = models.ForeignKey(ShippingBillingAddress, on_delete=models.SET_NULL, related_name="b_orders", null=True, blank=True)
    
    class Meta:
        db_table = "user_order"
