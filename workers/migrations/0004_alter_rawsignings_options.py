# Generated by Django 5.0 on 2024-01-09 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0003_rawsignings_normalized_date_signed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rawsignings',
            options={'verbose_name_plural': 'Raw signings'},
        ),
    ]
