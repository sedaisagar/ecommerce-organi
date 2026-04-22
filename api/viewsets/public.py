from rest_framework import generics, views

from api.serializers.product import DepartmentSerializer, ProductResponseSerializer, ProductSerializer, VariantWithDetailsSerializer
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
    queryset = Product.objects.filter().select_related("department").prefetch_related("variants")
    serializer_class = ProductResponseSerializer
    


# Multiple Ledger(s)

    # Shop 1
        # Person A1 (eSewa, Khalti, Bank, Cash)
        # Person B1 (eSewa, Khalti, Bank, Cash)
    # Shop 2 
        # Person A2 (eSewa, Khalti, Bank, Cash)
        # Person B2 (eSewa, Khalti, Bank, Cash)
    # Shop 3 
        # Person A3 (eSewa, Khalti, Bank, Cash)
        # Person B3 (eSewa, Khalti, Bank, Cash)