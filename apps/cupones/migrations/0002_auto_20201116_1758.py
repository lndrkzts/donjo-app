# Generated by Django 3.1.2 on 2020-11-16 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cupones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupon',
            name='descuento',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]