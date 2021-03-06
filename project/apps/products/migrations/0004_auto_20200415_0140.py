# Generated by Django 3.0.5 on 2020-04-14 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200414_0222'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='used_delay',
            field=models.BooleanField(default=False, verbose_name='Использывал допустимую отсрочку'),
        ),
        migrations.AlterField(
            model_name='product',
            name='buyback_date',
            field=models.DateField(verbose_name='Ожидаемая дата выкупа'),
        ),
    ]
