# Generated by Django 4.0.5 on 2022-08-25 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Web', '0002_system_dependences'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='system_dependences',
            options={'verbose_name_plural': 'System Dependencies'},
        ),
        migrations.CreateModel(
            name='CCTV_Cameras',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Ip_Address', models.GenericIPAddressField()),
                ('Admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]