# Generated by Django 4.2.8 on 2024-01-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_contactmodel_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='body_post',
            field=models.TextField(verbose_name='body_post'),
        ),
    ]
