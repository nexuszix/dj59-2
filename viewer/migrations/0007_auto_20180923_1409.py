# Generated by Django 2.1.1 on 2018-09-23 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0006_auto_20180923_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterstock',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='masterstock',
            name='stock_abbr',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
    ]