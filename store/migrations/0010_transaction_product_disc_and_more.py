# Generated by Django 5.0.1 on 2024-01-31 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_transaction_issued_to_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='product_disc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='issued_to_staff',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='product',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
