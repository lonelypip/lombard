# Generated by Django 3.0.5 on 2020-04-13 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.IntegerField(choices=[(0, 'В ожидании выкупа'), (1, 'В продаже'), (3, 'Продано'), (4, 'Выкуплено')], default=0),
        ),
    ]
