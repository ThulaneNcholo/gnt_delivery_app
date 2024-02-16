# Generated by Django 4.2.10 on 2024-02-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitemsmodel',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True),
        ),
        migrations.AddField(
            model_name='menuitemsmodel',
            name='sale_status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
