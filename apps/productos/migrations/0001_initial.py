# Generated by Django 3.1.2 on 2020-10-04 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('peso', models.DecimalField(decimal_places=2, max_digits=8)),
                ('unidad_peso', models.CharField(choices=[('GRAMO', 'Gramo'), ('KILO', 'Kilo'), ('LITRO', 'Litro')], max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('imagen', models.ImageField(upload_to='productos/')),
                ('slug', models.SlugField(unique=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
