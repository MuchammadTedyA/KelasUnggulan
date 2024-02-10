# Generated by Django 4.0.2 on 2023-06-02 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0027_delete_derajat_probabilitas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='derajat_probabilitas',
            fields=[
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('nilai', models.FloatField(null=True)),
                ('kriteria1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fahp.kriteria')),
            ],
        ),
    ]