# Generated by Django 4.2.10 on 2024-02-13 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('description', models.TextField(blank=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='static/images')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('item_ingredients', models.ManyToManyField(blank=True, default=None, related_name='item_ingredients', to='dishes.ingredientsmodel')),
            ],
        ),
    ]