# Generated by Django 5.0.1 on 2024-02-01 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='section_quantity',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='staff_quantity',
        ),
        migrations.AlterField(
            model_name='product',
            name='c_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.category'),
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_name', models.CharField(blank=True, max_length=100, null=True)),
                ('rec_quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
        ),
    ]