# Generated by Django 4.0.2 on 2023-06-08 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0045_rename_iq_huruf_siswa_siswa_iq_siswa_h'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hasil',
            old_name='id_subkriteria',
            new_name='subkriteria',
        ),
    ]
