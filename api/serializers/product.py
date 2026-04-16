import random

from rest_framework import serializers

from products.models import CouponCode, Departments, Product, VariantName, Variants
from django.utils.text import slugify

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = "__all__"

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def validate(self, attrs):
        
        slug = attrs.get("slug")
        name = attrs.get("name")

        if not slug:
            slug = slugify(name)
            if Departments.objects.filter(slug=slug).exists():
                slug = f"{slug}-{random.randint(999,999999999)}"
        
        attrs["slug"] = slug
        
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class VariantNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantName
        fields = "__all__"

class VariantsSerializer(serializers.ModelSerializer):
    variant_name = serializers.SerializerMethodField()

    class Meta:
        model = Variants
        fields = "__all__"

    def get_variant_name(self, instance:Variants):
        return instance.variant.name

    def to_representation(self, instance: Variants):
        data =  super().to_representation(instance)
        # data["variant_name"] = instance.variant.name
        return data

# class VariantWithDetailsSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = VariantName
    #     fields = "__all__"

    # def to_representation(self, instance:VariantName):
        # data =  super().to_representation(instance)
        # data["items"] = VariantsSerializer(instance.variants.all(), many=True).data
        # return data


class VariantWithDetailsSerializer(serializers.Serializer):
    
    def to_representation(self, instance:VariantName):
        data = {
            str(instance.name) : [i.name for i in instance.variants.all()]
        }
        return data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance:Product):
        data =  super().to_representation(instance)

        data.update(
            department=DepartmentSerializer(instance.department, context=self.context).data,
            variants= VariantsSerializer(instance.variants.all(), many=True, context=self.context).data
        )

        return data


class CouponCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CouponCode
        fields = "__all__"