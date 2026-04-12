from django.db import models


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # Creation ts
    updated_at = models.DateTimeField(auto_now=True) # Update ts

    publish = models.BooleanField(default=True)

    priority = models.PositiveIntegerField() # Highest comes first
    # order = models.PositiveIntegerField() # Low to high

    class Meta:
        abstract = True