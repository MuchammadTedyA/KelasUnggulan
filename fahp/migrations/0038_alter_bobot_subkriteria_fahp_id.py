# Generated by Django 4.0.2 on 2023-06-04 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0037_alter_bobot_subkriteria_fahp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bobot_subkriteria_fahp',
            name='id',
            field=models.CharField(max_length=9, primary_key=True, serialize=False),
        ),
    ]
