# Generated by Django 4.1.7 on 2023-03-02 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='date_upload',
            field=models.DateField(auto_now_add=True),
        ),
    ]
