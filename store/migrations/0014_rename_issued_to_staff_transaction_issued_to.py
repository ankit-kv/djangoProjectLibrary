# Generated by Django 5.0.1 on 2024-02-01 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_section_section_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='issued_to_staff',
            new_name='issued_to',
        ),
    ]
