from rest_framework import filters, generics, views

from api.filters.prod import ProductFilter
from api.serializers.product import DepartmentSerializer, ProductResponseSerializer, ProductSerializer, VariantWithDetailsSerializer
from products.models import Departments, Product, VariantName

from rest_framework.response import Response

from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from rest_framework.permissions import IsAuthenticatedOrReadOnly
@extend_schema(tags=["Public APIs"])
class DepartmentView(generics.ListAPIView):
    queryset = Departments.objects.filter(publish=True)
    serializer_class = DepartmentSerializer
    filterset_fields = ['name']
    search_fields = ['name']
    filter_backends = [filters.SearchFilter,filters.OrderingFilter, DjangoFilterBackend]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)    

@extend_schema(tags=["Public APIs"])
class VariantsView(views.APIView):
    def get(self, request, *args, **kwargs):
        queryset = VariantName.objects.filter(publish=True)
        serializer = VariantWithDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

@extend_schema(tags=["Public APIs"])
class ProductsView(generics.ListAPIView):
    queryset = Product.objects.filter(publish=True, department__publish=True).select_related("department").prefetch_related("variants")
    serializer_class = ProductResponseSerializer
    filterset_class = ProductFilter
    # throttle_scope = "anon"
    # permission_classes=[IsAuthenticatedOrReadOnly]

    # @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)    


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