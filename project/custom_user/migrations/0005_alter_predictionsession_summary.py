# Generated by Django 4.2.5 on 2024-07-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0004_predictionsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionsession',
            name='summary',
            field=models.JSONField(default=list),
        ),
    ]
