# Generated by Django 3.1.4 on 2021-01-03 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_auto_20210102_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='slug',
        ),
    ]