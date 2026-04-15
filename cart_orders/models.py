from django.db import models

from utils.models import CommonModel

class CartItems(CommonModel):
    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("products.Product",on_delete=models.CASCADE, related_name="cart_items")

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_items"


