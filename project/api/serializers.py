from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.products.models import Check, Product



class CheckSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def validate_code(self, code):
        if Check.objects.filter(code=code).exists():
            return code
        raise ValidationError('Такой код не существует')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name',
                  'description',
                  'photo',
                  'buyback_date',
                  'status',
                  'buyback_price',)
