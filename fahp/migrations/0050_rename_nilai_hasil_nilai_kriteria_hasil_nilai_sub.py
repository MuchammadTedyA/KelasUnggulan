# Generated by Django 4.0.2 on 2023-06-10 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fahp', '0049_alter_hasil_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hasil',
            old_name='nilai',
            new_name='nilai_kriteria',
        ),
        migrations.AddField(
            model_name='hasil',
            name='nilai_sub',
            field=models.FloatField(null=True),
        ),
    ]
