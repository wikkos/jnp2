# Generated by Django 2.0.6 on 2018-06-13 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='execution',
            name='sid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
