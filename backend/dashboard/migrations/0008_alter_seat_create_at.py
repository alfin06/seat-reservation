# Generated by Django 5.1.4 on 2025-05-22 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_reservationsetting_reset_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='create_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
