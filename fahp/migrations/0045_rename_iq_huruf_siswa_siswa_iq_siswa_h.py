# Generated by Django 4.0.2 on 2023-06-08 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0044_sub_kriteria_bobot_subkriteria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siswa',
            old_name='iq_huruf_siswa',
            new_name='iq_siswa_h',
        ),
    ]
