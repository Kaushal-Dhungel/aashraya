# Generated by Django 3.1.3 on 2021-02-25 11:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('searchingapp', '0002_auto_20210224_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='location_customised',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]