from django.db import models
from apps.products.models import Product, Delay
import datetime



class Buyout(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    price = models.IntegerField(
        default=0,
        verbose_name='Цена выкупа'
    )

    class Meta:
        verbose_name = 'Выкуп'
        verbose_name_plural = 'Выкупы'

    def __str__(self):
        return self.product.name

    def extend(self):
        self.product.buyback_date = self.productbuyback_date + datetime.timedelta(days=Delay.objects.first().days)
        self.save()
        return {
            'Сообщение':'Успешно',
            'Дата выкупа':self.product.buyback_date
        }


class Renewal(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    price = models.IntegerField(
        default=0,
        verbose_name='Цена продлевания'
    )

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Продлевание'
        verbose_name_plural = 'Продлевания'