# Generated by Django 4.2.8 on 2024-01-15 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_contactmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmodel',
            name='phone',
            field=models.CharField(max_length=100),
        ),
    ]
