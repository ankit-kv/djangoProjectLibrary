# Generated by Django 5.0.1 on 2024-02-08 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_request_items_date_time_request_items_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='request_items',
            name='tracking_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
