# Generated by Django 4.0.2 on 2022-12-11 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='derajat_probabilitas',
            fields=[
                ('id_drajatProb', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('id_kriteria1', models.CharField(max_length=2)),
                ('id_kriteria2', models.CharField(max_length=2)),
                ('nilai_prob', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='kriteria',
            fields=[
                ('id_kriteria', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('nama_kriteria', models.CharField(max_length=20)),
                ('bobot_kriteria', models.FloatField(default=0.0)),
                ('bobot_hasil_kriteria', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='siswa',
            fields=[
                ('nisn_siswa', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nama_siswa', models.CharField(max_length=50)),
                ('iq_siswa', models.CharField(max_length=3)),
                ('iq_huruf_siswa', models.CharField(max_length=2)),
                ('tpa_ipa_siswa', models.CharField(max_length=3)),
                ('tpa_ips_siswa', models.CharField(max_length=3)),
                ('tpa_bahasa_siswa', models.CharField(max_length=3)),
                ('rapor_ipa_siswa', models.CharField(max_length=3)),
                ('rapor_ips_siswa', models.CharField(max_length=3)),
                ('rapor_bahasa_siswa', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='sub_kriteria',
            fields=[
                ('id_subKriteria', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('nama_subKriteria', models.CharField(max_length=20)),
                ('bobot_subKriteria', models.FloatField(default=0.0)),
                ('bobot_hasil_subKriteria', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='hasil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_kriteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fahp.kriteria')),
                ('id_siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fahp.siswa')),
                ('id_subKriteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fahp.sub_kriteria')),
            ],
        ),
    ]
