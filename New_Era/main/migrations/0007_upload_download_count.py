# Generated by Django 4.2 on 2023-04-10 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_county_upload_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='download_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
