# Generated by Django 4.0.2 on 2023-05-28 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0006_alter_sub_kriteria_id_subkriteria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sub_kriteria',
            old_name='id_kriteria',
            new_name='kriteria',
        ),
    ]
