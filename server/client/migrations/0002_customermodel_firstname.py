# Generated by Django 4.2.10 on 2024-02-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermodel',
            name='firstName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
