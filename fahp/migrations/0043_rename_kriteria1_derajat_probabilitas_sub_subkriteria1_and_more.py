# Generated by Django 4.0.2 on 2023-06-05 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0042_alter_sum_kriteria_fahp_id_sum_subkriteria_fahp_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='derajat_probabilitas_sub',
            old_name='kriteria1',
            new_name='subkriteria1',
        ),
        migrations.RenameField(
            model_name='derajat_probabilitas_sub',
            old_name='kriteria2',
            new_name='subkriteria2',
        ),
    ]
