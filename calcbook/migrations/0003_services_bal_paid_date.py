# Generated by Django 3.0.7 on 2020-06-09 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcbook', '0002_service_sites_site_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='bal_paid_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
