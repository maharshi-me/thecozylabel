# Generated by Django 3.0.2 on 2020-09-25 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200925_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('N', 'New Arrivals (Show on Top)')], max_length=1),
        ),
    ]
