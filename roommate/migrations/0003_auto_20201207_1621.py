# Generated by Django 3.1.3 on 2020-12-07 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roommate', '0002_auto_20201120_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomieimage',
            name='roomie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='roommate.roomie'),
        ),
    ]
