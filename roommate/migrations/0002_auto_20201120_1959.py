# Generated by Django 3.1.3 on 2020-11-20 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roommate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomieimage',
            name='roomie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roomie_imgs', to='roommate.roomie'),
        ),
    ]