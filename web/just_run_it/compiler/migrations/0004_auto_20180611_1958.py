# Generated by Django 2.0.6 on 2018-06-11 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compiler', '0003_add_test_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='language',
            field=models.CharField(choices=[('C', 'gcc'), ('CPP17', 'g++17'), ('PYTHON3', 'python3')], default='C', max_length=10),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('SU', 'submitted'), ('OK', 'completed successfully')], default='SU', max_length=3),
        ),
    ]
