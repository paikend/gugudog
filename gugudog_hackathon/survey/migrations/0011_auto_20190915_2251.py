# Generated by Django 2.2.4 on 2019-09-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.CharField(max_length=500),
        ),
    ]