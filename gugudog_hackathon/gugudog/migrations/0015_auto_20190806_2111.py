# Generated by Django 2.2.4 on 2019-08-06 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gugudog', '0014_auto_20190806_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='logo_image',
            field=models.ImageField(blank=True, null=True, upload_to='logo_images'),
        ),
    ]