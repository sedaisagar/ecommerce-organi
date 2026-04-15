from rest_framework import generics, views

from api.serializers.product import DepartmentSerializer, ProductSerializer, VariantWithDetailsSerializer
from products.models import Departments, Product, VariantName

from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Public APIs"])
class DepartmentView(generics.ListAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer

@extend_schema(tags=["Public APIs"])
class VariantsView(views.APIView):
    def get(self, request, *args, **kwargs):
        queryset = VariantName.objects.all()
        serializer = VariantWithDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

@extend_schema(tags=["Public APIs"])
class ProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
