# Generated by Django 4.0.2 on 2023-05-29 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0015_sum_kriteria_ahp'),
    ]

    operations = [
        migrations.AddField(
            model_name='bobot_kriteria_ahp',
            name='normalisasi',
            field=models.FloatField(null=True),
        ),
    ]
