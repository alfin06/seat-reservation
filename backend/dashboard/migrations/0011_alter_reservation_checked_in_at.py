# Generated by Django 5.1.4 on 2025-05-22 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_reservation_checked_in_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='checked_in_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
