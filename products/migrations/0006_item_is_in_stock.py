# Generated by Django 3.0.2 on 2020-09-25 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200925_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_in_stock',
            field=models.BooleanField(default=True),
        ),
    ]