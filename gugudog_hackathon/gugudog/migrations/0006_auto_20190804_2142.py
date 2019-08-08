# Generated by Django 2.2.4 on 2019-08-04 12:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gugudog', '0005_service_zzim_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='gudog_users',
            field=models.ManyToManyField(blank=True, related_name='gudog_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='service',
            name='zzim_users',
            field=models.ManyToManyField(blank=True, related_name='zzim_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
