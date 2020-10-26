# Generated by Django 3.1.2 on 2020-10-26 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carritos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_pedido', models.CharField(max_length=100, unique=True)),
                ('estado', models.CharField(choices=[('Eliminado', 'Eliminado'), ('Creado', 'Creado'), ('Pago', 'Pago'), ('En Preparacion', 'En Preparacion'), ('Preparado', 'Preparado'), ('Enviado', 'Enviado'), ('Entregado', 'Entregado')], max_length=50)),
                ('costo_envio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carritos.carrito')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]