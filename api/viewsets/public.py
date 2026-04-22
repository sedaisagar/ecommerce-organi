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
    queryset = Product.objects.filter(publish=True).select_related("department").prefetch_related("variants")
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


from django.db import connection
class RawSqlTestView(generics.GenericAPIView):
    serializer_class = None

    def get_queryset(self):
        return super().get_queryset()


    def fetch_all_products(self):
        with connection.cursor() as cursor:
            cursor.execute("select id, name, slug, price, market_price from products where publish=%s", [True])
            row = cursor.fetchall()

        return row

    def get(self, request, *args, **kwargs):
        # RAW SQL WAY
        # prods = self.fetch_all_products()
        # prods = [{'id':i[0], 'name':i[1], 'slug':i[2], 'price':i[3], 'market_price':i[4]} for i in prods]

        # ORM WAY
        prods = Product.objects.filter(publish=True).values("id","name","slug","price", "market_price")
        
        return Response({"data":list(prods)})