# Generated by Django 5.0 on 2023-12-27 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(default='anonim_user.png', upload_to='profile_pictures/'),
        ),
    ]
