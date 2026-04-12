from rest_framework import viewsets

from api.serializers.product import DepartmentSerializer, VariantNameSerializer, VariantWithDetailsSerializer, VariantsSerializer
from products.models import Departments, VariantName, Variants
from utils.pagination import CustomPagination
from utils.permissions import IsAdminUser

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

@extend_schema(tags=["Admin APIs -  Department(s)"])
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]
    # pagination_class = CustomPagination


@extend_schema(tags=["Admin APIs -  VariantName(s)"])
class VariantNameViewSet(viewsets.ModelViewSet):
    queryset = VariantName.objects.all()
    serializer_class = VariantNameSerializer
    permission_classes = [IsAdminUser]
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "get_variants":
            return VariantWithDetailsSerializer
            
        return super().get_serializer_class()

    @action(methods=["GET"], detail=False, url_path="get-variants")
    def get_variants(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



@extend_schema(tags=["Admin APIs -  Variant(s)"])
class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variants.objects.all()
    serializer_class = VariantsSerializer
    permission_classes = [IsAdminUser]
    # pagination_class = CustomPagination



