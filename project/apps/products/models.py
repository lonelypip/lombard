from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime
import random



class DateModel(models.Model):
    created = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name='дата обновления',
        auto_now=True
    )

    class Meta:
        abstract = True


class Delay(models.Model):
    days = models.IntegerField()

    def __str__(self):
        return f'Второй шанс: {self.days} дней'

    def save(self, *args, **kwargs):
        if not self.pk and Delay.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError('Вы уже допустимое время отсрочки')
        return super(Delay, self).save(*args, **kwargs)



class Percent(models.Model):
    percent = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Процент за каждый день')

    def __str__(self):
        return f'В день {self.percent} процента'

    def save(self, *args, **kwargs):
        if not self.pk and Percent.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError('Вы уже указали процент')
        return super(Percent, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Процент в день'
        verbose_name_plural = 'Процент в день'


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})


class Check(models.Model):
    code = models.CharField(max_length=100)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return self.code


class Product(DateModel):
    STATUS = [
        (0, ('В ожидании выкупа')),
        (1, ('В продаже')),
        (3, ('Продано')),
        (4, ('Выкуплено'))
    ]
    check_code = models.ForeignKey(
        Check,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Номер чека'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    selling_price = models.IntegerField(
        verbose_name='Цена продажи'
    )
    photo = models.ImageField(
        default='default.png',
        upload_to='products',
        verbose_name='Фотография'
    )
    buyback_date = models.DateField(
        verbose_name='Ожидаемая дата выкупа'
    )
    purchase_price = models.IntegerField(
        verbose_name='Цена выплаты'
    )
    status = models.IntegerField(
        choices=STATUS,
        default=0,
        verbose_name='Статус'
    )
    offer = models.BooleanField(
        default=False,
        verbose_name='Топ'
    )
    used_delay = models.BooleanField(
        default=False,
        verbose_name='Использывал допустимую отсрочку'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    @property
    def buyback_price(self):
        if datetime.datetime.now().date() > self.buyback_date:
            self.status = 2
            self.save()
            days = datetime.datetime.now().date() - self.created.date()
        else:
            days = self.buyback_date - self.created.date()
        days = days.days
        money_per_day = (Percent.objects.first().percent * self.purchase_price) / 100
        return int(money_per_day * days + self.purchase_price)

    # @property
    # def extend_price(self):


    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.check_code is None:
            code = random.randint(10000000000, 99999999999)
            check = Check.objects.create(code=code)
            self.check_code = check
        # self.buyback_date + datetime.timedelta(days=Delay.objects.first().days)
        if self.used_delay == False:
            self.buyback_date = self.buyback_date + datetime.timedelta(days=Delay.objects.first().days)
            self.used_delay = True
        super(Product, self).save(*args, **kwargs)

    @property
    def may_extend(self):
        if (self.buyback_date - datetime.datetime.now().date()).days < 15:
            return True
        return False


