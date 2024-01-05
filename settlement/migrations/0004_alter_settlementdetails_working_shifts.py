# Generated by Django 5.0 on 2024-01-04 23:59

import django.core.serializers.json
import settlement.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settlement', '0003_settlementdetails_working_shifts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settlementdetails',
            name='working_shifts',
            field=models.JSONField(default=settlement.models.SettlementDetails.working_shifts_default, encoder=django.core.serializers.json.DjangoJSONEncoder),
        ),
    ]