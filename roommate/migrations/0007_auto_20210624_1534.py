# Generated by Django 3.1.3 on 2021-06-24 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roommate', '0006_roomiecartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomiecartitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_roomie', to='roommate.roomie'),
        ),
    ]