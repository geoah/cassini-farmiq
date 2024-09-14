# Generated by Django 5.1.1 on 2024-09-14 13:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonalevent',
            name='disease_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='seasonalevent',
            name='event_type',
            field=models.CharField(choices=[('soil_preparation', 'Soil Preparation'), ('germination', 'Germination'), ('planting', 'Planting'), ('fertilization', 'Fertilization'), ('pest_disease', 'Pest/Disease Presence'), ('weeding', 'Weeding'), ('pruning_trimming', 'Pruning/Trimming'), ('irrigation', 'Irrigation'), ('soil_test', 'Soil Test'), ('harvest', 'Harvest')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seasonalevent',
            name='fertilizer_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='seasonalevent',
            name='fertilizer_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='seasonalevent',
            name='harvest_yield',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='seasonalevent',
            name='irrigation_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='seasonalevent',
            name='pest_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='seasonalevent',
            name='soil_ph',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='seasonalevent',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]