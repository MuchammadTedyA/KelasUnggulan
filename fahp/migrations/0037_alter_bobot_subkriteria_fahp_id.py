# Generated by Django 4.0.2 on 2023-06-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0036_alter_sum_subkriteria_ahp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bobot_subkriteria_fahp',
            name='id',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
    ]
