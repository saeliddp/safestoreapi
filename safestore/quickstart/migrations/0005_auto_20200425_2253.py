# Generated by Django 3.0.5 on 2020-04-26 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0004_auto_20200425_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='latitude',
            field=models.CharField(default='0.000000', max_length=30),
        ),
        migrations.AlterField(
            model_name='store',
            name='longitude',
            field=models.CharField(default='0.000000', max_length=30),
        ),
    ]
