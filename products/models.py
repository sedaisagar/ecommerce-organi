from django.db import models

from utils.models import CommonModel
from django.utils.text import slugify

class Departments(CommonModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, null=True , blank=True)
    image = models.ImageField(upload_to="department-images/")

    class Meta:
        db_table = "departments"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class VariantName(CommonModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "variant_names"

class Variants(CommonModel):
    variant = models.ForeignKey(VariantName, on_delete=models.PROTECT, related_name="variants")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "variants"
    

# {
#     "Color":[
#         "Red", "Blue", "Black",
#     ],
#     "Size":[
#         "Xl", "XXL", "SM",
#     ],
#     "Ram":[
#         "4GB", "8GB", "12GB",
#     ],
# }



class Product(CommonModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, null=True , blank=True)

    image = models.ImageField(upload_to="product-images/")
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    market_price = models.DecimalField(max_digits=10, decimal_places=2)

    short_description = models.CharField(max_length=500)

    stock_quantity = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2) # Weight in KG

    description = models.TextField()
    information = models.TextField()

    department = models.ForeignKey(Departments, related_name="products", on_delete=models.PROTECT)
    variants = models.ManyToManyField(Variants, related_name="products", blank=True)


    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
