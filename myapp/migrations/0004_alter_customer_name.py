# Generated by Django 5.1.2 on 2025-01-18 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
