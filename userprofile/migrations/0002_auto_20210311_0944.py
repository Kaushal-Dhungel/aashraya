# Generated by Django 3.1.3 on 2021-03-11 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar/avatar.png', upload_to='avatars/'),
        ),
    ]