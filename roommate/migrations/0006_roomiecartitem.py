# Generated by Django 3.1.3 on 2021-02-27 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
        ('roommate', '0005_roomie_location_customised'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomieCartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart_roomie', to='roommate.roomie')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile')),
            ],
        ),
    ]
