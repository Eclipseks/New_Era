# Generated by Django 4.1.7 on 2023-03-02 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('brand', models.CharField(max_length=40)),
                ('county', models.CharField(max_length=5)),
                ('date_registr', models.CharField(max_length=20)),
                ('date_upload', models.DateTimeField(auto_now_add=True)),
                ('mpc1', models.FloatField()),
                ('mpc2', models.FloatField()),
                ('mpc3', models.FloatField()),
                ('mpc4', models.FloatField()),
            ],
        ),
    ]
