# Generated by Django 4.0.2 on 2023-05-21 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siswa',
            name='rapor_bahasa_siswa_h',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='siswa',
            name='rapor_ipa_siswa_h',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='siswa',
            name='rapor_ips_siswa_h',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='siswa',
            name='tpa_bahasa_siswa_h',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='siswa',
            name='tpa_ipa_siswa_h',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='siswa',
            name='tpa_ips_siswa_h',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
