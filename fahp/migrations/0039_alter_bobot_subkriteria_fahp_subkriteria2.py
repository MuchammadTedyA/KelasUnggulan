# Generated by Django 4.0.2 on 2023-06-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0038_alter_bobot_subkriteria_fahp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bobot_subkriteria_fahp',
            name='subkriteria2',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
