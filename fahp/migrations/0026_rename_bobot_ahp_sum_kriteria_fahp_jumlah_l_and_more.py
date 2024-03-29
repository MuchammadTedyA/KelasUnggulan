# Generated by Django 4.0.2 on 2023-06-01 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0025_remove_bobot_kriteria_fahp_jumlah_l_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sum_kriteria_fahp',
            old_name='bobot_ahp',
            new_name='jumlah_l',
        ),
        migrations.RenameField(
            model_name='sum_kriteria_fahp',
            old_name='sum_kosistensi',
            new_name='jumlah_m',
        ),
        migrations.RenameField(
            model_name='sum_kriteria_fahp',
            old_name='sum_kosistensi2',
            new_name='jumlah_u',
        ),
        migrations.RemoveField(
            model_name='sum_kriteria_fahp',
            name='sum_ahp',
        ),
        migrations.AddField(
            model_name='sum_kriteria_fahp',
            name='si_l',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='sum_kriteria_fahp',
            name='si_m',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='sum_kriteria_fahp',
            name='si_u',
            field=models.FloatField(null=True),
        ),
    ]
