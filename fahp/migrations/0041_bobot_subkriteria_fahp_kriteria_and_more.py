# Generated by Django 4.0.2 on 2023-06-04 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0040_bobot_subkriteria_ahp_kriteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='bobot_subkriteria_fahp',
            name='kriteria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fahp.kriteria'),
        ),
        migrations.AddField(
            model_name='sum_subkriteria_ahp',
            name='kriteria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fahp.kriteria'),
        ),
    ]
