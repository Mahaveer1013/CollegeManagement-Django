# Generated by Django 5.0.7 on 2024-07-25 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_staff_pdf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='pdf',
            new_name='resume',
        ),
    ]