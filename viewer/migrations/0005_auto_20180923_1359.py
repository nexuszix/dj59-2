# Generated by Django 2.1.1 on 2018-09-23 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_auto_20180923_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdata',
            name='remark',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
