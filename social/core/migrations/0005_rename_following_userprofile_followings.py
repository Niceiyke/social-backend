# Generated by Django 4.1.3 on 2023-03-19 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='following',
            new_name='followings',
        ),
    ]
