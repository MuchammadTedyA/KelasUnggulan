# Generated by Django 4.0.2 on 2023-06-15 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0051_alter_siswa_iq_siswa_alter_siswa_rapor_bahasa_siswa_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='laporan_hasil',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='laporan_hasil_d',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nilai_sub1', models.FloatField()),
                ('nilai_kriteria1', models.FloatField()),
                ('nilai_sub2', models.FloatField()),
                ('nilai_kriteria2', models.FloatField()),
                ('nilai_sub3', models.FloatField()),
                ('nilai_kriteria3', models.FloatField()),
                ('nilai_sum', models.FloatField()),
                ('kriteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fahp.kriteria')),
                ('laporan_hasil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fahp.laporan_hasil')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fahp.siswa')),
            ],
        ),
    ]
