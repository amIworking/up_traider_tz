# Generated by Django 4.2.6 on 2023-10-26 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='nested_level',
            field=models.SmallIntegerField(default=0, verbose_name='Nested Level'),
        ),
    ]
