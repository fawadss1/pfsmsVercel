# Generated by Django 4.0.5 on 2022-08-25 17:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Web', '0003_alter_system_dependences_options_cctv_cameras'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CCTV_Cameras',
            new_name='CCTV_Camera',
        ),
    ]
