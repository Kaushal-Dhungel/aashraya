# Generated by Django 3.1.3 on 2021-02-25 11:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('roommate', '0004_auto_20210224_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomie',
            name='location_customised',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
