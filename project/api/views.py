from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from apps.products.models import Product, Check
from .serializers import CheckSerializer, ProductSerializer





class CheckViewSet(ViewSet):
    serializer_class = CheckSerializer

    def products(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        check = Check.objects.get(code=serializer.validated_data['code'])
        products = Product.objects.filter(check_code=check)
        product_serializer = ProductSerializer(products, many=True).data
        return Response(status=status.HTTP_200_OK, data=product_serializer)

